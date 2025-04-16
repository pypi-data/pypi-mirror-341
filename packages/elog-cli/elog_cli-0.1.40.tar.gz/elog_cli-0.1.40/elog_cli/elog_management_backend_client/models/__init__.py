"""Contains all the data models used in inputs/outputs"""

from .api_result_response_application_details_dto import ApiResultResponseApplicationDetailsDTO
from .api_result_response_attachment_dto import ApiResultResponseAttachmentDTO
from .api_result_response_boolean import ApiResultResponseBoolean
from .api_result_response_entry_dto import ApiResultResponseEntryDTO
from .api_result_response_entry_processing_stats_dto import ApiResultResponseEntryProcessingStatsDTO
from .api_result_response_group_details_dto import ApiResultResponseGroupDetailsDTO
from .api_result_response_list_application_details_dto import ApiResultResponseListApplicationDetailsDTO
from .api_result_response_list_attachment_dto import ApiResultResponseListAttachmentDTO
from .api_result_response_list_entry_summary_dto import ApiResultResponseListEntrySummaryDTO
from .api_result_response_list_group_details_dto import ApiResultResponseListGroupDetailsDTO
from .api_result_response_list_logbook_dto import ApiResultResponseListLogbookDTO
from .api_result_response_list_tag_dto import ApiResultResponseListTagDTO
from .api_result_response_list_user_details_dto import ApiResultResponseListUserDetailsDTO
from .api_result_response_logbook_dto import ApiResultResponseLogbookDTO
from .api_result_response_string import ApiResultResponseString
from .api_result_response_tag_dto import ApiResultResponseTagDTO
from .api_result_response_user_details_dto import ApiResultResponseUserDetailsDTO
from .application_details_dto import ApplicationDetailsDTO
from .attachment_dto import AttachmentDTO
from .authorization_group_management_dto import AuthorizationGroupManagementDTO
from .details_authorization_dto import DetailsAuthorizationDTO
from .details_authorization_dto_owner_type import DetailsAuthorizationDTOOwnerType
from .details_authorization_dto_permission import DetailsAuthorizationDTOPermission
from .details_authorization_dto_resource_type import DetailsAuthorizationDTOResourceType
from .entry_dto import EntryDTO
from .entry_import_dto import EntryImportDTO
from .entry_new_dto import EntryNewDTO
from .entry_processing_stats_dto import EntryProcessingStatsDTO
from .entry_summary_dto import EntrySummaryDTO
from .get_all_logbook_filter_for_authorization_types import GetAllLogbookFilterForAuthorizationTypes
from .group_details_dto import GroupDetailsDTO
from .import_entry_dto import ImportEntryDTO
from .logbook_dto import LogbookDTO
from .logbook_shift_dto import LogbookShiftDTO
from .logbook_summary_dto import LogbookSummaryDTO
from .new_application_dto import NewApplicationDTO
from .new_attachment_body import NewAttachmentBody
from .new_authorization_dto import NewAuthorizationDTO
from .new_authorization_dto_owner_type import NewAuthorizationDTOOwnerType
from .new_authorization_dto_permission import NewAuthorizationDTOPermission
from .new_authorization_dto_resource_type import NewAuthorizationDTOResourceType
from .new_entry_dto import NewEntryDTO
from .new_entry_with_attachment_body import NewEntryWithAttachmentBody
from .new_local_group_dto import NewLocalGroupDTO
from .new_logbook_dto import NewLogbookDTO
from .new_tag_dto import NewTagDTO
from .shift_dto import ShiftDTO
from .summarizes_dto import SummarizesDTO
from .tag_dto import TagDTO
from .update_authorization_dto import UpdateAuthorizationDTO
from .update_authorization_dto_permission import UpdateAuthorizationDTOPermission
from .update_local_group_dto import UpdateLocalGroupDTO
from .update_logbook_dto import UpdateLogbookDTO
from .update_tag_dto import UpdateTagDTO
from .upload_entry_and_attachment_1_body import UploadEntryAndAttachment1Body
from .upload_entry_and_attachment_body import UploadEntryAndAttachmentBody
from .user_details_dto import UserDetailsDTO

__all__ = (
    "ApiResultResponseApplicationDetailsDTO",
    "ApiResultResponseAttachmentDTO",
    "ApiResultResponseBoolean",
    "ApiResultResponseEntryDTO",
    "ApiResultResponseEntryProcessingStatsDTO",
    "ApiResultResponseGroupDetailsDTO",
    "ApiResultResponseListApplicationDetailsDTO",
    "ApiResultResponseListAttachmentDTO",
    "ApiResultResponseListEntrySummaryDTO",
    "ApiResultResponseListGroupDetailsDTO",
    "ApiResultResponseListLogbookDTO",
    "ApiResultResponseListTagDTO",
    "ApiResultResponseListUserDetailsDTO",
    "ApiResultResponseLogbookDTO",
    "ApiResultResponseString",
    "ApiResultResponseTagDTO",
    "ApiResultResponseUserDetailsDTO",
    "ApplicationDetailsDTO",
    "AttachmentDTO",
    "AuthorizationGroupManagementDTO",
    "DetailsAuthorizationDTO",
    "DetailsAuthorizationDTOOwnerType",
    "DetailsAuthorizationDTOPermission",
    "DetailsAuthorizationDTOResourceType",
    "EntryDTO",
    "EntryImportDTO",
    "EntryNewDTO",
    "EntryProcessingStatsDTO",
    "EntrySummaryDTO",
    "GetAllLogbookFilterForAuthorizationTypes",
    "GroupDetailsDTO",
    "ImportEntryDTO",
    "LogbookDTO",
    "LogbookShiftDTO",
    "LogbookSummaryDTO",
    "NewApplicationDTO",
    "NewAttachmentBody",
    "NewAuthorizationDTO",
    "NewAuthorizationDTOOwnerType",
    "NewAuthorizationDTOPermission",
    "NewAuthorizationDTOResourceType",
    "NewEntryDTO",
    "NewEntryWithAttachmentBody",
    "NewLocalGroupDTO",
    "NewLogbookDTO",
    "NewTagDTO",
    "ShiftDTO",
    "SummarizesDTO",
    "TagDTO",
    "UpdateAuthorizationDTO",
    "UpdateAuthorizationDTOPermission",
    "UpdateLocalGroupDTO",
    "UpdateLogbookDTO",
    "UpdateTagDTO",
    "UploadEntryAndAttachment1Body",
    "UploadEntryAndAttachmentBody",
    "UserDetailsDTO",
)
