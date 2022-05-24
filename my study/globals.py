

from modules.preference.models.preference_user_value import PreferenceUserValue
from modules.preference.models.preference_value import PreferenceUser
from modules.user.models.user_account import UserAccount
from modules.user.models.user_active_history import UserActiveHistory
from modules.user.models.user_level import UserLevel
from modules.user.models.user_permission import UserPermission
from modules.file.models.file_temporary import FileTemporary
from modules.hierarchy.models.hierarchies import HierarchyItem
from modules.hierarchy.models.hierarchies import HierarchyOption
from modules.hierarchy.models.hierarchies import HierarchyGroup
from modules.mail.models.mail_account import MailAccount
from modules.mail.models.mail_template import MailTemplate
from modules.mail.models.mail_confirmer import MailConfirmer
from modules.user.models.user_permission_value import UserPermissionValue
from modules.user.exports import export_models



TableService = {
    # UserActiveHistory.__tablename__,
    # PreferenceUserValue.__tablename__,
    UserAccount.__tablename__,
    UserLevel.__tablename__
    # PreferenceUser.__tablename__,
    # UserPermission.__tablename__,
    # FileTemporary.__tablename__,
    # HierarchyItem.__tablename__,
    # HierarchyOption.__tablename__,
    # HierarchyGroup.__tablename__,
    # MailAccount.__tablename__,
    # MailTemplate.__tablename__,
    # MailConfirmer.__tablename__,
    # UserPermissionValue.__tablename__

}