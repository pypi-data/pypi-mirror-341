# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class LocalDestination:
    # Storage type. This could be [LOCAL/S3/SFTP/AZURE]
    backup_dest: Optional[str] = _field(default=None, metadata={"alias": "backupDest"})
    # Location where the database backup file on a storage type.
    backup_dir: Optional[str] = _field(default=None, metadata={"alias": "backupDir"})
    # Size of the database backup allowed to the stored at a backup destination
    backup_storage_in_gb: Optional[int] = _field(
        default=None, metadata={"alias": "backupStorageInGB"}
    )
    # Time to live for a database backup copy in the backup destination in days
    backup_ttl_in_days: Optional[int] = _field(default=None, metadata={"alias": "backupTTLInDays"})
    # Number of replicas of the database backup file
    num_of_replica: Optional[int] = _field(default=None, metadata={"alias": "numOfReplica"})
    # vManage software version against which the database backup was taken
    vm_version: Optional[str] = _field(default=None, metadata={"alias": "vmVersion"})


@dataclass
class LocalBackupInfo:
    """
    List of all local backup info objects in the system
    """

    # Current stage of database backup workflow. This could be [SCHEDULED/IN_PROGRESS/CONFIG_DB_BACKUP_SUCCESS/CONFIG_DB_BACKUP_FAILED/STATS_DB_EXPORT_SUCCESS/STATS_DB_EXPORT_FAILED/CONFIG_DB_CONSISTENCY_CHECK_FAILED/LEADER_SUCCESS/ALL_SUCCESS/FAILURE/DELETED]
    backup_state: Optional[str] = _field(default=None, metadata={"alias": "backupState"})
    # Type of backup. This could be [SCHEDULED/ON_DEMAND]
    backup_type: Optional[str] = _field(default=None, metadata={"alias": "backupType"})
    # Epoch timestamp
    create_time: Optional[int] = _field(default=None, metadata={"alias": "createTime"})
    destination: Optional[LocalDestination] = _field(default=None)
    # Destination to download database backup from
    download_url: Optional[str] = _field(default=None, metadata={"alias": "downloadURL"})
    # List of vManage servers IP address who are running in follower mode
    follower_ip_address_list: Optional[List[str]] = _field(
        default=None, metadata={"alias": "followerIpAddressList"}
    )
    # A unique UUID per database back up request
    local_backup_info_id: Optional[str] = _field(
        default=None, metadata={"alias": "localBackupInfoId"}
    )
    # A unique UUID for scheduled database backup task
    schedule_id: Optional[str] = _field(default=None, metadata={"alias": "scheduleId"})
    # IP address of the source vmanage server for database backup
    src_ip_address: Optional[str] = _field(default=None, metadata={"alias": "srcIpAddress"})
    # Unique task Id for a given database backup task
    task_id: Optional[str] = _field(default=None, metadata={"alias": "taskId"})
    # Task name in human readable format
    task_name: Optional[str] = _field(default=None, metadata={"alias": "taskName"})


@dataclass
class LocalBackupListResult:
    # List of all local backup info objects in the system
    backup_list: Optional[List[LocalBackupInfo]] = _field(
        default=None, metadata={"alias": "backupList"}
    )
