-- Example code to create the ZTF candidate_images table
-- Partition key is object id
-- Clustering key is jd

CREATE TABLE candidate_images (
    candid bigint,
    filename ascii,
    type ascii,
    filenameimage blob,
    PRIMARY KEY (candid)
);
