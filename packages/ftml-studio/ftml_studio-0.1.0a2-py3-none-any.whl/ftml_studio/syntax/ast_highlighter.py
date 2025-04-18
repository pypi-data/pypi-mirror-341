# src/ftml_studio/syntax/ast_highlighter.py
import logging
import re
import time

from PySide6.QtCore import QRegularExpression, QTimer, Signal, QObject
from PySide6.QtGui import QTextCharFormat, QColor

import ftml
from ftml.exceptions import FTMLParseError
from ftml.parser.ast import KeyValueNode, ScalarNode, ObjectNode, ListNode

from .base_highlighter import BaseHighlighter

# Configure logging
logger = logging.getLogger("ftml_ast_highlighter")


# Helper class to emit signals (since QSyntaxHighlighter doesn't inherently support signals)
class ErrorSignaler(QObject):
    errorsChanged = Signal(list)  # Signal emitted when errors change


class FTMLASTHighlighter(BaseHighlighter):
    """AST-based syntax highlighter for FTML documents with theme support and error resilience"""

    def __init__(self, document, theme_manager=None, error_highlighting=True, parse_delay=500,
                 highlight_error_delay=2000):
        logger.debug("Initializing FTMLASTHighlighter")
        super().__init__(document, theme_manager)

        # Create signal emitter for errors
        self._signaler = ErrorSignaler()
        self.errorsChanged = self._signaler.errorsChanged
        logger.debug("Error signaler created")

        # Configure options
        self.error_highlighting = error_highlighting  # Whether to highlight errors directly
        self.parse_delay = parse_delay  # Delay in milliseconds before parsing after content change
        self.highlight_error_delay = highlight_error_delay  # Delay before showing errors
        self.last_activity_ts = time.time()  # Track when the user was last active
        logger.debug(
            f"Configuration: error_highlighting={error_highlighting}, parse_delay={parse_delay}"
            f"ms, highlight_error_delay={highlight_error_delay}ms")

        # Initialize formats specific to AST highlighting
        self.initialize_ast_formats()
        logger.debug("AST formats initialized")

        # Analysis timer to prevent excessive parsing attempts while typing
        self.parse_timer = QTimer()
        self.parse_timer.setSingleShot(True)
        self.parse_timer.timeout.connect(self.parse_document)
        logger.debug("Parse timer created and connected")

        # Error display timer to show errors after inactivity
        self.error_display_timer = QTimer()
        self.error_display_timer.setSingleShot(True)
        self.error_display_timer.timeout.connect(self.rehighlight)
        logger.debug("Error display timer created and connected")

        # Current AST and parse errors
        self.ast = None
        self.parse_error = None
        self.errors = []

        # The document content that was successfully parsed
        self.valid_content = ""

        # A flag to indicate if we're using partial highlighting
        self.using_partial_highlighting = False

        # Start initial parsing timer
        logger.debug("Connecting contentsChange signal")
        self.document().contentsChange.connect(self.handle_content_change)
        logger.debug(f"Starting initial parse timer with delay {self.parse_delay}ms")
        self.parse_timer.start(self.parse_delay)  # Parse after delay
        logger.debug("FTMLASTHighlighter initialization complete")

    def initialize_ast_formats(self):
        """Initialize text formats for AST-specific elements using theme"""
        logger.debug("Initializing AST formats")
        # Create formats using theme semantic roles
        self._create_format("key", role="keyword", bold=True)
        self._create_format("equals", role="operator", bold=True)
        self._create_format("string", role="string")
        self._create_format("number", role="number")
        self._create_format("boolean", role="boolean", bold=True)
        self._create_format("null", role="null", bold=True)
        self._create_format("symbol", role="symbol")
        self._create_format("comment", role="comment", italic=True)
        self._create_format("doc_comment", role="docComment", italic=True)
        self._create_format("inner_doc_comment", role="docComment", italic=True)
        self._create_format("outer_doc_comment", role="docComment", italic=True)
        self._create_format("error_token", role="error")  # For highlighting error tokens in red
        logger.debug("Base formats created")

        # Special handling for error format - use wave underline
        error_format = QTextCharFormat()
        if self.theme_manager:
            # Get error color from theme manager
            error_color = QColor(self.theme_manager.get_syntax_color("error"))
            logger.debug(f"Using theme error color: {error_color.name()}")
        else:
            # Fallback to bright red if no theme manager
            error_color = QColor("#ff0000")  # Default red
            logger.debug("No theme manager, using default red color for errors")

        # Set up distinctive error formatting
        error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        error_format.setUnderlineColor(error_color)

        # Light background to highlight error position
        background_color = QColor(error_color)
        background_color.setAlpha(20)  # Very transparent
        error_format.setBackground(background_color)

        # Store the format
        self.formats["error"] = error_format
        logger.debug("Error format initialized with wave underline")

    def handle_content_change(self, position, removed, added):
        """Handle document content changes"""
        logger.debug(f"Content changed: position={position}, removed={removed}, added={added}")

        # Update the last activity timestamp
        self.last_activity_ts = time.time()

        # Cancel any pending error display
        self.error_display_timer.stop()

        # Reset the timer to parse after delay of inactivity
        logger.debug(f"Restarting parse timer with delay {self.parse_delay}ms")
        self.parse_timer.start(self.parse_delay)

    def set_parse_delay(self, delay_ms):
        """Set the delay before parsing after content changes"""
        old_delay = self.parse_delay
        self.parse_delay = max(100, delay_ms)  # Ensure minimum 100ms delay
        logger.debug(f"Parse delay changed from {old_delay}ms to {self.parse_delay}ms")

    def parse_document(self):
        """Parse the entire document to build AST"""
        logger.debug("=== STARTING DOCUMENT PARSE ===")

        # Add a check to verify document exists
        doc = self.document()
        if doc is None:
            logger.error("Document is None, cannot parse")
            return

        content = doc.toPlainText()
        logger.debug(f"Document length: {len(content)} characters")

        # Reset errors and flags
        old_errors = self.errors.copy()
        old_error_count = len(old_errors)
        self.errors = []
        self.using_partial_highlighting = False
        self.valid_content = content  # Assume content is valid until proven otherwise
        logger.debug(f"Reset state: old_errors={old_error_count}, using_partial_highlighting=False")

        if not content.strip():
            logger.debug("Empty document, skipping parse")
            self.ast = None
            self.parse_error = None
            self.rehighlight()

            # Emit errors changed signal if errors were cleared
            if old_errors and not self.errors:
                logger.debug("Cleared errors, emitting errorsChanged signal")
                self._signaler.errorsChanged.emit(self.errors)
            return

        try:
            # Try to parse using FTML
            logger.debug("Attempting to parse FTML content")
            data = ftml.load(content, preserve_comments=True)
            logger.debug("FTML load successful")

            # Extract the AST from the returned data
            if hasattr(data, "_ast_node"):
                self.ast = data._ast_node
                self.parse_error = None
                logger.debug("Successfully parsed FTML document with AST")
            else:
                # If AST is not available, use partial highlighting
                self.ast = None
                self.using_partial_highlighting = True
                logger.debug("Parsed FTML but AST not available, using partial highlighting")

        except FTMLParseError as e:
            # Handle parse error - still try to partially highlight
            logger.debug(f"FTMLParseError caught: {str(e)}")
            self.ast = None
            self.parse_error = e
            self.using_partial_highlighting = True
            logger.debug("Set using_partial_highlighting=True due to parse error")

            # Extract line and column from error message if available
            error_msg = str(e)
            # Try to extract line and column from the message
            line_match = re.search(r'at line (\d+)', error_msg)
            col_match = re.search(r'col (\d+)', error_msg)

            if line_match and col_match:
                line = int(line_match.group(1))
                col = int(col_match.group(1))
                logger.debug(f"Extracted from error message: line={line}, col={col}")

                error_info = {
                    "line": line,
                    "col": col,
                    "message": error_msg,
                    "length": 1  # Default to 1 character
                }

                # Try to find the specific error token
                token_match = re.search(r'Got\s+\w+\s+([^\s]+)', error_msg)
                if token_match:
                    error_token = token_match.group(1)
                    error_info["token"] = error_token
                    error_info["length"] = len(error_token)
                    logger.debug(f"Extracted error token: '{error_token}', length={len(error_token)}")

                # Add the error to our list
                self.errors.append(error_info)
                logger.debug(f"Added error at line {line}, col {col}")

                # If we have an error location, try to highlight content up to that point
                logger.debug("Attempting to create partial valid content up to error")
                content_lines = content.splitlines()
                valid_lines = content_lines[:line - 1]  # Lines before error

                if line <= len(content_lines):
                    # Add the portion of the error line up to the error
                    error_line = content_lines[line - 1]
                    if col <= len(error_line):
                        valid_lines.append(error_line[:col - 1])

                self.valid_content = '\n'.join(valid_lines)

                # Try to parse the valid portion, if possible
                try:
                    if self.valid_content:
                        logger.debug("Attempting to parse valid portion")
                        partial_data = ftml.load(self.valid_content, preserve_comments=True)
                        if hasattr(partial_data, "_ast_node"):
                            self.ast = partial_data._ast_node
                            logger.debug("Successfully parsed partial FTML document")
                except Exception as parse_e:
                    logger.debug(f"Failed to parse partial content: {str(parse_e)}")
                    self.ast = None
            else:
                # If we couldn't extract line/col from the message, create a generic error
                logger.debug("Couldn't extract line/col from error message, creating generic error")
                self.errors.append({
                    "line": 1,
                    "col": 1,
                    "message": error_msg,
                    "length": 1
                })

        except Exception as e:
            # Handle other errors - fall back to regex highlighting
            logger.error(f"Unexpected error parsing FTML: {str(e)}", exc_info=True)
            self.ast = None
            self.parse_error = e
            self.using_partial_highlighting = True
            logger.debug("Set using_partial_highlighting=True due to unexpected error")

            # Add a generic error
            self.errors.append({
                "line": 1,
                "col": 1,
                "message": f"Unexpected error: {str(e)}",
                "length": 1
            })
            logger.debug("Added generic error at line 1, col 1")

        # Emit signal if errors changed
        if old_errors != self.errors:
            logger.debug(f"Errors changed from {old_error_count} to {len(self.errors)}, emitting signal")
            self._signaler.errorsChanged.emit(self.errors)
        else:
            logger.debug("No change in errors, not emitting signal")

        # Reapply highlighting after any change (success or failure)
        logger.debug("Calling rehighlight")
        self.rehighlight()
        logger.debug("=== DOCUMENT PARSE COMPLETE ===")

        # If we have errors, schedule the error display timer
        if self.errors:
            elapsed_ms = (time.time() - self.last_activity_ts) * 1000
            remaining_delay = max(0, self.highlight_error_delay - elapsed_ms)
            if remaining_delay > 0:
                logger.debug(f"Scheduling error display in {remaining_delay:.0f}ms")
                self.error_display_timer.start(int(remaining_delay))

        # Emit signal if errors were added or removed
        if old_errors != self.errors:
            logger.debug(f"Errors changed from {len(old_errors)} to {len(self.errors)}, emitting signal")
            for err in self.errors:
                logger.debug(f"Error to highlight: {err}")
            self._signaler.errorsChanged.emit(self.errors)
        else:
            logger.debug("No change in errors, not emitting signal")

        # Reapply highlighting after any change (success or failure)
        logger.debug("Calling rehighlight")

    def highlightBlock(self, text):
        """Apply highlighting to the given block of text"""
        block_number = self.currentBlock().blockNumber() + 1  # 1-based line numbers
        logger.debug(f"Highlighting block {block_number}: '{text[:20]}{'...' if len(text) > 20 else ''}'")

        # Set default block state
        self.setCurrentBlockState(0)

        # Always highlight comments first - these should always be highlighted
        # even if AST highlighting fails
        logger.debug(f"Highlighting comments for block {block_number}")
        self.highlight_comments(text)

        # Apply AST-based highlighting if available
        if self.ast:
            try:
                logger.debug(f"Using AST-based highlighting for block {block_number}")
                self.apply_ast_highlighting(text)
            except Exception as e:
                logger.error(f"Error in AST highlighting for block {block_number}: {str(e)}", exc_info=True)
                # If AST highlighting fails, we'll still have comment highlighting
        elif self.using_partial_highlighting:
            logger.debug(f"Using fallback highlighting for block {block_number}")
            # Fall back to regex-based highlighting for core elements
            self.apply_fallback_highlighting(text)

        # Always highlight errors if error highlighting is enabled
        if self.error_highlighting:
            logger.debug(f"Checking for errors on block {block_number}, total errors: {len(self.errors)}")
            self.highlight_errors(text)
        else:
            logger.debug("Error highlighting is disabled")

    def highlight_comments(self, text):
        """Highlight all types of comments while avoiding those inside string literals"""
        block_number = self.currentBlock().blockNumber() + 1

        # First identify all string literals to avoid processing comments within them
        string_regions = []

        # Find double-quoted strings
        dquote_regex = QRegularExpression(r'"(?:\\.|[^"\\])*"')
        match_iterator = dquote_regex.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            string_regions.append((match.capturedStart(), match.capturedEnd()))

        # Find single-quoted strings
        squote_regex = QRegularExpression(r"'(''|[^'])*'")
        match_iterator = squote_regex.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            string_regions.append((match.capturedStart(), match.capturedEnd()))

        # Helper function to check if a position is inside any string
        def is_in_string(pos):
            for start, end in string_regions:
                if start <= pos < end:
                    return True
            return False

        # Regular comments //
        comment_regex = QRegularExpression(r'//(?![!/]).*$')
        match_iterator = comment_regex.globalMatch(text)
        comment_count = 0
        while match_iterator.hasNext():
            match = match_iterator.next()
            comment_pos = match.capturedStart()

            # Only highlight if the comment is not inside a string
            if not is_in_string(comment_pos):
                self.setFormat(comment_pos, match.capturedLength(), self.formats["comment"])
                comment_count += 1

        # Inner doc comments //!
        inner_doc_regex = QRegularExpression(r'//!.*$')
        match_iterator = inner_doc_regex.globalMatch(text)
        inner_doc_count = 0
        while match_iterator.hasNext():
            match = match_iterator.next()
            comment_pos = match.capturedStart()

            # Only highlight if the comment is not inside a string
            if not is_in_string(comment_pos):
                self.setFormat(comment_pos, match.capturedLength(), self.formats["inner_doc_comment"])
                inner_doc_count += 1

        # Outer doc comments ///
        outer_doc_regex = QRegularExpression(r'///.*$')
        match_iterator = outer_doc_regex.globalMatch(text)
        outer_doc_count = 0
        while match_iterator.hasNext():
            match = match_iterator.next()
            comment_pos = match.capturedStart()

            # Only highlight if the comment is not inside a string
            if not is_in_string(comment_pos):
                self.setFormat(comment_pos, match.capturedLength(), self.formats["outer_doc_comment"])
                outer_doc_count += 1

        if comment_count + inner_doc_count + outer_doc_count > 0:
            logger.debug(
                f"Block {block_number}: Found {comment_count} regular comments, {inner_doc_count} inner doc comments, "
                f"{outer_doc_count} outer doc comments")

    def apply_ast_highlighting(self, text):
        """Apply highlighting based on AST nodes"""
        block_number = self.currentBlock().blockNumber() + 1  # 1-based line numbers
        logger.debug(f"Applying AST highlighting to block {block_number}")

        # Process all elements on this line
        self.process_elements_on_line(self.ast, text, block_number)

    def apply_fallback_highlighting(self, text):
        """Apply basic highlighting when AST is not available"""
        block_number = self.currentBlock().blockNumber() + 1
        logger.debug(f"Applying fallback highlighting to block {block_number}")

        # This is a simplified fallback that uses regex patterns for basic highlighting
        formats_applied = 0

        # ================================================================
        # Keys and equals signs (both regular and quoted)
        # ================================================================

        # 1. First handle quoted keys - these need to be processed before string values
        # Match double-quoted keys at the start of a line, followed by =
        dquoted_key_regex = QRegularExpression(r'^[ \t]*("(?:\\.|[^"\\])*")[ \t]*(?==)')
        match_iterator = dquoted_key_regex.globalMatch(text)
        key_count = 0
        while match_iterator.hasNext():
            match = match_iterator.next()
            # Highlight the entire quoted key (including quotes) as a key
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.formats["key"])
            key_count += 1
            formats_applied += 1

            # Find the equals sign after the key
            equals_regex = QRegularExpression(r"=")
            equals_match = equals_regex.match(text, match.capturedEnd(1))
            if equals_match.hasMatch():
                self.setFormat(equals_match.capturedStart(), equals_match.capturedLength(), self.formats["equals"])
                formats_applied += 1

        # Match single-quoted keys at the start of a line, followed by =
        squoted_key_regex = QRegularExpression(r"^[ \t]*('(''|[^'])*')[ \t]*(?==)")
        match_iterator = squoted_key_regex.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            # Highlight the entire quoted key (including quotes) as a key
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.formats["key"])
            key_count += 1
            formats_applied += 1

            # Find the equals sign after the key
            equals_regex = QRegularExpression(r"=")
            equals_match = equals_regex.match(text, match.capturedEnd(1))
            if equals_match.hasMatch():
                self.setFormat(equals_match.capturedStart(), equals_match.capturedLength(), self.formats["equals"])
                formats_applied += 1

        # 2. Then handle regular unquoted keys
        key_regex = QRegularExpression(r"^[ \t]*([A-Za-z_][A-Za-z0-9_]*)[ \t]*(?==)")
        match_iterator = key_regex.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            # Highlight the key
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.formats["key"])
            key_count += 1
            formats_applied += 1

            # Find the equals sign after the key
            equals_regex = QRegularExpression(r"=")
            equals_match = equals_regex.match(text, match.capturedEnd(1))
            if equals_match.hasMatch():
                self.setFormat(equals_match.capturedStart(), equals_match.capturedLength(), self.formats["equals"])
                formats_applied += 1

        # ================================================================
        # Strings - AFTER keys but BEFORE numbers to ensure correct precedence
        # ================================================================
        # Skip any text already formatted (to avoid highlighting keys as strings)

        # Helper function to check if a range has existing formatting
        def is_range_formatted(start, length):
            for i in range(start, start + length):
                if i < len(text) and self.format(i) != QTextCharFormat():
                    return True
            return False

        # Double-quoted strings (with escape sequences)
        string_regex = QRegularExpression(r'"(?:\\.|[^"\\])*"')
        match_iterator = string_regex.globalMatch(text)
        string_count = 0
        while match_iterator.hasNext():
            match = match_iterator.next()
            # Only highlight as string if not already formatted (as a key)
            if not is_range_formatted(match.capturedStart(), match.capturedLength()):
                self.setFormat(match.capturedStart(), match.capturedLength(), self.formats["string"])
                string_count += 1
                formats_applied += 1

        # Single-quoted strings (with proper escaping)
        single_quote_regex = QRegularExpression(r"'(''|[^'])*'")
        match_iterator = single_quote_regex.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            # Only highlight as string if not already formatted (as a key)
            if not is_range_formatted(match.capturedStart(), match.capturedLength()):
                self.setFormat(match.capturedStart(), match.capturedLength(), self.formats["string"])
                string_count += 1
                formats_applied += 1

        # ================================================================
        # Numbers - AFTER strings so they don't override string formatting
        # ================================================================
        # Integer numbers
        number_regex = QRegularExpression(r'\b-?\d+\b')
        match_iterator = number_regex.globalMatch(text)
        number_count = 0
        while match_iterator.hasNext():
            match = match_iterator.next()
            # Only apply number formatting to text not already formatted
            if not is_range_formatted(match.capturedStart(), match.capturedLength()):
                self.setFormat(match.capturedStart(), match.capturedLength(), self.formats["number"])
                number_count += 1
                formats_applied += 1

        # Floating point numbers
        float_regex = QRegularExpression(r'\b-?\d+\.\d+\b')
        match_iterator = float_regex.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            # Only apply number formatting to text not already formatted
            if not is_range_formatted(match.capturedStart(), match.capturedLength()):
                self.setFormat(match.capturedStart(), match.capturedLength(), self.formats["number"])
                number_count += 1
                formats_applied += 1

        # ================================================================
        # Booleans and null
        # ================================================================
        # Boolean values
        boolean_regex = QRegularExpression(r'\b(true|false)\b')
        match_iterator = boolean_regex.globalMatch(text)
        bool_count = 0
        while match_iterator.hasNext():
            match = match_iterator.next()
            if not is_range_formatted(match.capturedStart(), match.capturedLength()):
                self.setFormat(match.capturedStart(), match.capturedLength(), self.formats["boolean"])
                bool_count += 1
                formats_applied += 1

        # Null value
        null_regex = QRegularExpression(r'\bnull\b')
        match_iterator = null_regex.globalMatch(text)
        null_count = 0
        while match_iterator.hasNext():
            match = match_iterator.next()
            if not is_range_formatted(match.capturedStart(), match.capturedLength()):
                self.setFormat(match.capturedStart(), match.capturedLength(), self.formats["null"])
                null_count += 1
                formats_applied += 1

        # ================================================================
        # Braces, brackets and commas
        # ================================================================
        # Braces
        symbol_count = 0
        for i, char in enumerate(text):
            if char in "{},[]":
                # Only format symbols not already formatted
                if self.format(i) == QTextCharFormat():
                    self.setFormat(i, 1, self.formats["symbol"])
                    symbol_count += 1
                    formats_applied += 1

        if formats_applied > 0:
            logger.debug(
                f"Block {block_number}: Applied fallback formatting - {key_count} keys, {string_count} strings, "
                f"{number_count} numbers, {bool_count} booleans, {null_count} nulls, {symbol_count} symbols")

    def process_elements_on_line(self, node, text, block_number):
        """
        Process all elements in the AST that might be on the current line.
        This includes top-level items and nested items.
        """
        logger.debug(f"Processing AST elements on line {block_number}")
        elements_found = 0

        # Process root level items
        if hasattr(node, "items") and isinstance(node.items, dict):
            logger.debug(f"Node has {len(node.items)} items")
            for key, kv_node in node.items.items():
                # Process the key-value pair itself if it's on this line
                if hasattr(kv_node, 'line') and kv_node.line == block_number:
                    logger.debug(f"Found key-value node for key '{key}' on line {block_number}")
                    self.process_key_value_node(kv_node, text)
                    elements_found += 1

                # Even if the key-value pair itself isn't on this line,
                # its value might have elements on this line
                if hasattr(kv_node, 'value'):
                    if isinstance(kv_node.value, ObjectNode):
                        if self.process_object_node(kv_node.value, text, block_number):
                            elements_found += 1
                    elif isinstance(kv_node.value, ListNode):
                        if self.process_list_node(kv_node.value, text, block_number):
                            elements_found += 1

                # Process comments
                if hasattr(kv_node, "leading_comments"):
                    for comment in kv_node.leading_comments:
                        if hasattr(comment, 'line') and comment.line == block_number:
                            logger.debug(f"Found leading comment on line {block_number}")
                            self.highlight_comment_node(comment, text)
                            elements_found += 1

                if (hasattr(kv_node, "inline_comment") and
                        kv_node.inline_comment and
                        hasattr(kv_node.inline_comment, 'line') and
                        kv_node.inline_comment.line == block_number):
                    logger.debug(f"Found inline comment on line {block_number}")
                    self.highlight_comment_node(kv_node.inline_comment, text)
                    elements_found += 1

        logger.debug(f"Found {elements_found} AST elements on line {block_number}")
        return elements_found > 0

    def process_key_value_node(self, node, text):
        """Process a key-value node, highlighting the key, equals sign and value"""
        if not isinstance(node, KeyValueNode):
            logger.debug("Not a KeyValueNode, skipping")
            return

        # Get the key and look for it in different forms
        key = node.key
        logger.debug(f"Processing key: '{key}'")

        # Look for potential quoted forms of the key in the text
        dquoted_key = f'"{key}"'
        squoted_key = f"'{key}'"

        # Try to find the key in the text - first check quoted forms
        key_pos = -1
        key_length = 0

        if dquoted_key in text:
            # Found double-quoted key
            key_pos = text.find(dquoted_key)
            key_length = len(dquoted_key)
            logger.debug(f"Found double-quoted key at position {key_pos}")
            self.setFormat(key_pos, key_length, self.formats["key"])
        elif squoted_key in text:
            # Found single-quoted key
            key_pos = text.find(squoted_key)
            key_length = len(squoted_key)
            logger.debug(f"Found single-quoted key at position {key_pos}")
            self.setFormat(key_pos, key_length, self.formats["key"])
        else:
            # Look for unquoted key
            key_pos = text.find(key)
            key_length = len(key)

            # Only apply formatting if we found the key and it's at a word boundary
            if key_pos >= 0:
                # Check if it's at a word boundary (start of line or after whitespace)
                at_boundary = (key_pos == 0 or text[key_pos - 1].isspace())

                if at_boundary:
                    logger.debug(f"Found unquoted key at position {key_pos}")
                    self.setFormat(key_pos, key_length, self.formats["key"])
                else:
                    logger.debug(f"Found key but not at word boundary, position {key_pos}")
                    key_pos = -1  # Reset as we didn't find a valid key position
            else:
                logger.debug(f"Key '{key}' not found in text")
                key_pos = -1

        # Highlight equals sign if we found a valid key position
        if key_pos >= 0:
            # Look for equals sign after the key
            equals_pos = text.find("=", key_pos + key_length)
            if equals_pos >= 0:
                logger.debug(f"Highlighting equals sign at position {equals_pos}")
                self.setFormat(equals_pos, 1, self.formats["equals"])

                # Highlight value if it's a scalar
                if node.value and isinstance(node.value, ScalarNode):
                    logger.debug(f"Processing scalar value of type {type(node.value.value).__name__}")
                    # Pass the full text and the position after equals sign
                    self.highlight_value_node(node.value, text, starting_pos=equals_pos + 1)
            else:
                logger.debug("Equals sign not found")

    def process_object_node(self, node, text, block_number):
        """Process an object node, looking for elements on the current line"""
        if not isinstance(node, ObjectNode):
            logger.debug("Not an ObjectNode, skipping")
            return False

        elements_found = 0
        # Highlight braces if they're on this line
        if hasattr(node, 'line') and node.line == block_number:
            # Opening brace is on this line
            lbrace_pos = text.find("{")
            if lbrace_pos >= 0:
                logger.debug(f"Highlighting opening brace at position {lbrace_pos}")
                self.setFormat(lbrace_pos, 1, self.formats["symbol"])
                elements_found += 1
            else:
                logger.debug("Opening brace not found in text")

        # Check for closing brace on this line
        # This is a simplification - we'd need more info to know for sure
        # if a closing brace belongs to this specific object
        rbrace_pos = text.rfind("}")
        if rbrace_pos >= 0:
            logger.debug(f"Highlighting closing brace at position {rbrace_pos}")
            self.setFormat(rbrace_pos, 1, self.formats["symbol"])
            elements_found += 1
        else:
            logger.debug("Closing brace not found in text")

        # Process items in the object
        if hasattr(node, 'items'):
            logger.debug(f"Object has {len(node.items)} items")
            for key, item_node in node.items.items():
                # Check if this key-value pair is on this line
                if hasattr(item_node, 'line') and item_node.line == block_number:
                    logger.debug(f"Found item with key '{key}' on line {block_number}")

                    # Look for potential quoted forms of the key in the text
                    dquoted_key = f'"{key}"'
                    squoted_key = f"'{key}'"

                    # Try to find the key in the text - first check quoted forms
                    key_pos = -1
                    key_length = 0

                    if dquoted_key in text:
                        # Found double-quoted key
                        key_pos = text.find(dquoted_key)
                        key_length = len(dquoted_key)
                        logger.debug(f"Found double-quoted key at position {key_pos}")
                        self.setFormat(key_pos, key_length, self.formats["key"])
                    elif squoted_key in text:
                        # Found single-quoted key
                        key_pos = text.find(squoted_key)
                        key_length = len(squoted_key)
                        logger.debug(f"Found single-quoted key at position {key_pos}")
                        self.setFormat(key_pos, key_length, self.formats["key"])
                    else:
                        # Look for unquoted key
                        key_pos = text.find(key)
                        key_length = len(key)
                        if key_pos >= 0:
                            logger.debug(f"Highlighting key '{key}' at position {key_pos}")
                            self.setFormat(key_pos, key_length, self.formats["key"])
                        else:
                            logger.debug(f"Key '{key}' not found in text")
                            key_pos = -1

                    # Highlight equals sign
                    if key_pos >= 0:
                        equals_pos = text.find("=", key_pos + key_length)
                        if equals_pos >= 0:
                            logger.debug(f"Highlighting equals sign at position {equals_pos}")
                            self.setFormat(equals_pos, 1, self.formats["equals"])
                            elements_found += 1

                            # Highlight the value after the equals sign
                            if item_node.value:
                                logger.debug(f"Processing value of type {type(item_node.value).__name__}")

                                # For scalar values, highlight appropriately
                                if isinstance(item_node.value, ScalarNode):
                                    # Pass the full text and the position after equals sign
                                    self.highlight_value_node(item_node.value, text, starting_pos=equals_pos + 1)
                                    elements_found += 1
                        else:
                            logger.debug("Equals sign not found")

                # Check for nested objects and lists
                if hasattr(item_node, 'value'):
                    if isinstance(item_node.value, ObjectNode):
                        if self.process_object_node(item_node.value, text, block_number):
                            elements_found += 1
                    elif isinstance(item_node.value, ListNode):
                        if self.process_list_node(item_node.value, text, block_number):
                            elements_found += 1

                # Process comments
                if hasattr(item_node, "leading_comments"):
                    for comment in item_node.leading_comments:
                        if hasattr(comment, 'line') and comment.line == block_number:
                            logger.debug(f"Found leading comment on line {block_number}")
                            self.highlight_comment_node(comment, text)
                            elements_found += 1

                if hasattr(item_node, "inline_comment") and item_node.inline_comment and hasattr(
                        item_node.inline_comment, 'line') and item_node.inline_comment.line == block_number:
                    logger.debug(f"Found inline comment on line {block_number}")
                    self.highlight_comment_node(item_node.inline_comment, text)
                    elements_found += 1

        return elements_found > 0

    def process_list_node(self, node, text, block_number):
        """Process a list node, looking for elements on the current line"""
        if not isinstance(node, ListNode):
            logger.debug("Not a ListNode, skipping")
            return False

        elements_found = 0
        # Highlight brackets if they're on this line
        if hasattr(node, 'line') and node.line == block_number:
            # Opening bracket is on this line
            lbracket_pos = text.find("[")
            if lbracket_pos >= 0:
                logger.debug(f"Highlighting opening bracket at position {lbracket_pos}")
                self.setFormat(lbracket_pos, 1, self.formats["symbol"])
                elements_found += 1
            else:
                logger.debug("Opening bracket not found in text")

        # Check for closing bracket on this line
        rbracket_pos = text.rfind("]")
        if rbracket_pos >= 0:
            logger.debug(f"Highlighting closing bracket at position {rbracket_pos}")
            self.setFormat(rbracket_pos, 1, self.formats["symbol"])
            elements_found += 1
        else:
            logger.debug("Closing bracket not found in text")

        # Highlight commas on this line
        comma_count = 0
        for i, char in enumerate(text):
            if char == ',':
                logger.debug(f"Highlighting comma at position {i}")
                self.setFormat(i, 1, self.formats["symbol"])
                comma_count += 1
                elements_found += 1

        if comma_count > 0:
            logger.debug(f"Highlighted {comma_count} commas")

        # Process elements in the list
        if hasattr(node, 'elements'):
            logger.debug(f"List has {len(node.elements)} elements")

            # Find all strings in the text for later matching
            string_matches = []
            double_quote_pattern = QRegularExpression(r'"(?:\\.|[^"\\])*"')
            single_quote_pattern = QRegularExpression(r"'(''|[^'])*'")

            match_iterator = double_quote_pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                string_matches.append((match.capturedStart(), match.capturedEnd(), match.captured()))

            match_iterator = single_quote_pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                string_matches.append((match.capturedStart(), match.capturedEnd(), match.captured()))

            # Sort by position so we can find them in order
            string_matches.sort()

            for elem in node.elements:
                # Check if this element is on this line
                if hasattr(elem, 'line') and elem.line == block_number:
                    # Handle string list elements with special care
                    if isinstance(elem, ScalarNode) and isinstance(elem.value, str):
                        # Find this string element in our collected matches
                        elem_str = elem.value
                        logger.debug(f"Looking for string list element: '{elem_str}'")

                        # Try to find this element value in our collected string matches
                        for start, end, captured in string_matches:
                            # Check if this captured string has our element's value
                            # (removing quotes and handling escapes)
                            if captured.startswith('"') and captured.endswith('"'):
                                # Double-quoted string
                                unquoted = captured[1:-1].replace('\\"', '"')
                                if unquoted == elem_str:
                                    logger.debug(f"Found string list element at {start}-{end}: {captured}")
                                    self.setFormat(start, end - start, self.formats["string"])
                                    elements_found += 1
                                    break
                            elif captured.startswith("'") and captured.endswith("'"):
                                # Single-quoted string
                                unquoted = captured[1:-1].replace("''", "'")
                                if unquoted == elem_str:
                                    logger.debug(f"Found string list element at {start}-{end}: {captured}")
                                    self.setFormat(start, end - start, self.formats["string"])
                                    elements_found += 1
                                    break
                    else:
                        # For non-string elements, use regular highlighting
                        logger.debug("Processing non-string list element")
                        self.highlight_value_node(elem, text)
                        elements_found += 1

                # Check for nested objects and lists
                if isinstance(elem, ObjectNode):
                    if self.process_object_node(elem, text, block_number):
                        elements_found += 1
                elif isinstance(elem, ListNode):
                    if self.process_list_node(elem, text, block_number):
                        elements_found += 1

        return elements_found > 0

    def highlight_value_node(self, node, text, starting_pos=0):
        """Highlight a scalar value node with position awareness"""
        if not isinstance(node, ScalarNode):
            logger.debug(f"Not a ScalarNode, got {type(node).__name__}")
            return

        # CRITICAL: Order matters here - check specific types before general types
        # 1. String values
        if isinstance(node.value, str):
            value_str = node.value
            logger.debug(f"Processing string value: '{value_str[:20]}{'...' if len(value_str) > 20 else ''}'")

            # Find quoted form of the string in the text after starting_pos
            dquoted_value = f'"{value_str}"'
            squoted_value = f"'{value_str}'"

            # First try double quotes
            pos = text.find(dquoted_value, starting_pos)
            if pos >= 0:
                logger.debug(f"Found double-quoted string at position {pos}")
                self.setFormat(pos, len(dquoted_value), self.formats["string"])
                return

            # Then try single quotes
            pos = text.find(squoted_value, starting_pos)
            if pos >= 0:
                logger.debug(f"Found single-quoted string at position {pos}")
                self.setFormat(pos, len(squoted_value), self.formats["string"])
                return

            # If we didn't find an exact match, try regular expressions
            logger.debug("No exact string match, trying regex patterns")
            double_quote_pattern = QRegularExpression(r'"(?:\\.|[^"\\])*"')
            single_quote_pattern = QRegularExpression(r"'(''|[^'])*'")

            # Only search after starting position
            match_iterator = double_quote_pattern.globalMatch(text, starting_pos)
            while match_iterator.hasNext():
                match = match_iterator.next()
                # Extract the content without quotes to compare
                content = match.captured()
                if content.startswith('"') and content.endswith('"'):
                    content = content[1:-1].replace('\\"', '"')
                    if content == value_str:
                        logger.debug(f"Found matching double-quoted string via regex at {match.capturedStart()}")
                        self.setFormat(match.capturedStart(), match.capturedLength(), self.formats["string"])
                        return

            match_iterator = single_quote_pattern.globalMatch(text, starting_pos)
            while match_iterator.hasNext():
                match = match_iterator.next()
                content = match.captured()
                if content.startswith("'") and content.endswith("'"):
                    content = content[1:-1].replace("''", "'")
                    if content == value_str:
                        logger.debug(f"Found matching single-quoted string via regex at {match.capturedStart()}")
                        self.setFormat(match.capturedStart(), match.capturedLength(), self.formats["string"])
                        return

            logger.debug(f"Could not find matching string value in text: '{value_str}'")

        # 2. Boolean values
        elif isinstance(node.value, bool):
            # Find boolean value in the text
            value_str = str(node.value).lower()  # FTML uses lowercase true/false
            logger.debug(f"Processing boolean value: {value_str}")
            pos = text.find(value_str, starting_pos)
            if pos >= 0:
                logger.debug(f"Highlighting boolean at position {pos}")
                self.setFormat(pos, len(value_str), self.formats["boolean"])
            else:
                logger.debug(f"Boolean '{value_str}' not found in text")

        # 3. Null values
        elif node.value is None:
            # Find "null" in the text
            logger.debug("Processing null value")
            pos = text.find("null", starting_pos)
            if pos >= 0:
                logger.debug(f"Highlighting null at position {pos}")
                self.setFormat(pos, 4, self.formats["null"])
            else:
                logger.debug("'null' not found in text")

        # 4. Number values - check last so it doesn't try to find booleans as numbers
        elif isinstance(node.value, (int, float)):
            # Find the number in the text
            value_str = str(node.value)
            logger.debug(f"Processing number value: {value_str}")
            pos = text.find(value_str, starting_pos)
            if pos >= 0:
                logger.debug(f"Highlighting number at position {pos}")
                self.setFormat(pos, len(value_str), self.formats["number"])
            else:
                logger.debug(f"Number '{value_str}' not found in text")

    def highlight_comment_node(self, comment, text):
        """Highlight a comment node"""
        if not comment:
            logger.debug("No comment to highlight")
            return

        # Get the comment text
        comment_text = getattr(comment, 'text', '')
        if not comment_text:
            logger.debug("Comment has no text")
            return

        # Determine comment format based on type - default to regular comment
        format_key = "comment"  # Changed from "doc_comment" to "comment" as default

        if comment_text.startswith("//!"):
            logger.debug(f"Identified //! comment: {comment_text}")
            format_key = "inner_doc_comment"
        elif comment_text.startswith("///"):
            logger.debug(f"Identified /// comment: {comment_text}")
            format_key = "outer_doc_comment"
        else:
            logger.debug(f"Identified regular comment: {comment_text}")

        logger.debug(
            f"Using format key: {format_key} for comment: '{comment_text[:20]}"
            f"{'...' if len(comment_text) > 20 else ''}'")

        # Find the exact comment in the current line
        comment_pos = text.find(comment_text)
        if comment_pos >= 0:
            logger.debug(f"Found exact comment text at position {comment_pos}")
            self.setFormat(comment_pos, len(comment_text), self.formats[format_key])
        else:
            # If exact match fails, try to find the comment prefix
            if comment_text.startswith("//!"):
                prefix = "//!"
            elif comment_text.startswith("///"):
                prefix = "///"
            else:
                prefix = "//"

            comment_pos = text.find(prefix)
            if comment_pos >= 0:
                logger.debug(f"Found comment prefix '{prefix}' at position {comment_pos}")
                # Only highlight from the comment prefix to the end of the line
                self.setFormat(comment_pos, len(text) - comment_pos, self.formats[format_key])
            else:
                logger.debug(f"Comment prefix '{prefix}' not found in text")

    def highlight_errors(self, text):
        """Highlight parse errors in the text with wave underlines or themed highlighting"""
        block_number = self.currentBlock().blockNumber() + 1

        # Only process if error highlighting is enabled
        if not self.error_highlighting:
            logger.debug("Error highlighting is disabled")
            return

        if not self.errors:
            logger.debug("No errors to highlight")
            return

        # Check if enough time has passed since last activity
        current_time = time.time()
        elapsed_ms = (current_time - self.last_activity_ts) * 1000  # Convert to milliseconds

        if elapsed_ms < self.highlight_error_delay:
            logger.debug(
                f"Skipping error highlighting: only {elapsed_ms:.0f}ms since last activity "
                f"(need {self.highlight_error_delay}ms)")
            return

        """Highlight parse errors in the text with wave underlines or themed highlighting"""
        block_number = self.currentBlock().blockNumber() + 1

        # Only process if error highlighting is enabled
        if not self.error_highlighting:
            logger.debug("Error highlighting is disabled")
            return

        if not self.errors:
            logger.debug("No errors to highlight")
            return

        # Log for debugging
        logger.debug(f"Checking for errors on line {block_number}, errors count: {len(self.errors)}")

        for error in self.errors:
            logger.debug(f"Checking error: {error}")
            if error["line"] == block_number:
                logger.debug(f"Found error on line {block_number}: {error}")

                # Get error position and adjust if needed
                col = max(0, error["col"] - 1)  # Convert 1-based to 0-based, ensure not negative
                length = max(1, error.get("length", 1))  # Use length from error or default to 1

                logger.debug(f"Initial error position: col={col}, length={length}")

                # Check if position is at or beyond last non-whitespace character
                trimmed_text = text.rstrip()
                trimmed_length = len(trimmed_text)

                # If error position is beyond last meaningful character or at the very end
                if col >= trimmed_length:
                    logger.debug(f"Error position {col} is beyond last meaningful character (at {trimmed_length})")

                    # If we have non-empty text, highlight the last character
                    if trimmed_length > 0:
                        col = trimmed_length - 1
                        length = 1
                        logger.debug(f"Adjusted to highlight last character at position {col}")
                    else:
                        # If line is completely empty, highlight position 0
                        col = 0
                        length = 1
                        logger.debug("Empty line, highlighting position 0")

                # Try to find the specific error token if it's provided
                elif "token" in error:
                    # Look for this token in the text
                    error_token = error["token"]
                    logger.debug(f"Looking for error token: '{error_token}'")
                    token_pos = text.find(error_token, col)
                    if token_pos >= 0:
                        # Found the token, use its position and length
                        logger.debug(f"Found error token '{error_token}' at position {token_pos}")
                        col = token_pos
                        length = len(error_token)
                    else:
                        logger.debug(f"Error token '{error_token}' not found in text at col {col}")
                        # Try finding it anywhere in the line
                        token_pos = text.find(error_token)
                        if token_pos >= 0:
                            logger.debug(f"Found error token '{error_token}' at alternate position {token_pos}")
                            col = token_pos
                            length = len(error_token)
                        else:
                            logger.debug("Error token not found anywhere in line, using default position")

                # Check if position is within text bounds
                if col < len(text):
                    # Adjust length to not go beyond end of line
                    length = min(length, len(text) - col)

                    # Get the text being highlighted
                    error_text = text[col:col + length]
                    logger.debug(f"Highlighting error text: '{error_text}' at col {col}, length {length}")

                    # Create a direct error format
                    error_format = QTextCharFormat()
                    error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)

                    # Use theme-based error color instead of hardcoded red
                    if self.theme_manager:
                        error_color = QColor(self.theme_manager.get_syntax_color("error"))
                        background_color = QColor(error_color)
                        background_color.setAlpha(20)  # Very transparent
                    else:
                        # Fallback to default red if theme manager not available
                        error_color = QColor("#ff0000")  # Bright red
                        background_color = QColor("#ffeeee")  # Very light red

                    error_format.setUnderlineColor(error_color)
                    error_format.setBackground(background_color)

                    # Apply error format directly
                    logger.debug(f"Applying error format at col {col}, length {length}, color: {error_color.name()}")
                    self.setFormat(col, length, error_format)

                    # Set block state to indicate error
                    self.setCurrentBlockState(1)  # Use state 1 to indicate error
                    logger.debug(f"Set block state to 1 for error on line {block_number}")
                else:
                    logger.debug(f"Error position {col} is outside text bounds (length={len(text)})")
