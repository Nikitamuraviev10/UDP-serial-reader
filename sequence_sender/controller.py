import logging

from sequence_sender.model import SequenceSenderModel
from sequence_sender.view import SequenceSenderView

class SequenceSenderController:
    def __init__(self, model: SequenceSenderModel, view: SequenceSenderView):
        self.model = model
        self.view = view
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self._connect_signals()

    def _connect_signals(self):
        self.view.file_selected.connect(self.handle_file_selected)

    def handle_file_selected(self, file_path: str):
        try:
            self.model.load_config(file_path)
            self.view.update_output("Config loaded successfully")
        except Exception as e:
            self.logger.error(str(e))
            self.view.show_error(str(e))

