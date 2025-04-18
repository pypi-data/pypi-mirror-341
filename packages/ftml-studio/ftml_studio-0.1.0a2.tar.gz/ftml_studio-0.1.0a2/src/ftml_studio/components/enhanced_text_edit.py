# src/ftml_studio/ui/components/enhanced_text_edit.py
import logging
from PySide6.QtWidgets import QTextEdit, QToolTip

logger = logging.getLogger("enhanced_text_edit")


class EnhancedTextEdit(QTextEdit):
    """Enhanced QTextEdit with improved tooltip support for error indicators"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        # Store multiple errors instead of just one
        self.error_positions = []  # List of {position, message} dictionaries
        self.error_selections = []
        self.highlighter = None

    def setHighlighter(self, highlighter):
        """Store reference to the highlighter"""
        self.highlighter = highlighter

    def mouseMoveEvent(self, event):
        """Handle mouse movement to show tooltips over error positions"""
        super().mouseMoveEvent(event)

        if not self.error_positions:
            QToolTip.hideText()
            return

        cursor = self.cursorForPosition(event.pos())
        pos = cursor.position()

        # Check if cursor is near any error position
        for error in self.error_positions:
            error_pos = error.get('position', -1)
            error_msg = error.get('message', '')

            # Check if cursor is near the error position (within 5 characters)
            # This makes it easier to trigger the tooltip
            if error_pos >= 0 and abs(error_pos - pos) <= 5:
                # Only show/update tooltip if text changed or position changed significantly
                current_text = QToolTip.text()
                if current_text != error_msg or not QToolTip.isVisible():
                    logger.debug(f"Showing error tooltip at position {pos}: {error_msg}")
                    QToolTip.showText(event.globalPos(), error_msg)
                    return
                return

        # Hide tooltip if not over an error
        if QToolTip.isVisible():
            QToolTip.hideText()

    def setExtraSelections(self, selections):
        """Override to log extra selections being applied"""
        logger.debug(f"Setting {len(selections)} extra selections")
        self.error_selections = selections
        super().setExtraSelections(selections)

    def setHighlighterParent(self, parent):
        """Set the parent widget that owns the highlighter"""
        self.highlighter_parent = parent
