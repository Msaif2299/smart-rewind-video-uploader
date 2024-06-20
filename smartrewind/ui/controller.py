from smartrewind.ui.button_upload_video_file import UploadVideoFileButton
from smartrewind.ui.button_collection_folder import ChooseCollectionFolderButton
from smartrewind.ui.button_metadata_file_storage import ChooseMetadataFileStorageButton
from smartrewind.ui.button_start_process import StartProcessButton
from smartrewind.ui.model import Model

class Controller:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.set_metadata_generation_buttons()
        self.model.refresh_generation_objects_signal.connect(self.refresh_metadata_generation_buttons)

    def set_metadata_generation_buttons(self):
        self.upload_video_file = UploadVideoFileButton(self.model)
        self.choose_collection_folder = ChooseCollectionFolderButton(self.model)
        self.choose_metadata_file_storage_loc = ChooseMetadataFileStorageButton(self.model)
        self.start_process_button = StartProcessButton(self.model)
    
    def refresh_metadata_generation_buttons(self):
        self.upload_video_file.set_text(self.model.video_file_location)
        self.choose_collection_folder.set_text(self.model.collection_folder_location)
        self.choose_metadata_file_storage_loc.set_text(self.model.metadata_file_storage_location)