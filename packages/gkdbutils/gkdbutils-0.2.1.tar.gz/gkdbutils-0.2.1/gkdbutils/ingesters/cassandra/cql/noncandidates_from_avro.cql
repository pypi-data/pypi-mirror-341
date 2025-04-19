-- Example code to create the ZTF noncandidates table
-- Partition key is object id
-- Clustering key is jd

CREATE TABLE noncandidates (
    objectId ascii,
    jd double,
    fid int,
    diffmaglim float,
    nid int,
    field int,
    magzpsci float,
    magzpsciunc float,
    magzpscirms float,
    PRIMARY KEY (objectId, jd)
);
