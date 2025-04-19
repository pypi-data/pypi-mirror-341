CREATE TABLE cutouts.cutouts ("cutoutId" ascii,
                              cutoutimage blob,
                              imjd int,
                              "objectId" bigint,
PRIMARY KEY ("cutoutId", imjd)
)
WITH compaction={'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy', 'compaction_window_size': '1', 'compaction_window_unit': 'DAYS'}
AND default_time_to_live=86400;


WITH compaction={'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy', 'compaction_window_size': '1', 'compaction_window_unit': 'DAYS'}
AND default_time_to_live=7776000;


