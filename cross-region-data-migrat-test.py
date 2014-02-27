#! /usr/bin/env python
import os
from swift.common.ring import Ring

swift_dir="/etc/swift"
swift_dir1="/etc/swift/v1"
swift_dir2="/etc/swift/v2"

def count_migration():
    ring_v1=Ring(swift_dir1, ring_name='object')
    ring_v2=Ring(swift_dir2, ring_name='object')
    global_migrate_count=0
    local_migrate_count=0
    region_diff=0
    c=0
    f=open("/root/migrate.record","r+")
    for part in range(len(ring_v1._replica2part2dev_id[0])):
        region1_v1=0
        region1_v2=0
        for r in range(3):
            c=c+1
            dev_id_1=ring_v1._replica2part2dev_id[r][part]
            dev_id_2=ring_v2._replica2part2dev_id[r][part]
            if ring_v1.devs[dev_id_1]["region"]== 1:
                region1_v1=region1_v1+1
            if ring_v2.devs[dev_id_2]["region"]== 1:
                region1_v2=region1_v2+1
            if ring_v1.devs[dev_id_1]["region"] !=ring_v2.devs[dev_id_2]["region"] and ring_v1.devs[dev_id_1]["id"] !=ring_v2.devs[dev_id_2]["id"]:
                global_migrate_count=global_migrate_count+1
                record= str(ring_v1.devs[dev_id_1])+"from" +str(ring_v1.devs[dev_id_1]["region"])+" to "+ str(ring_v2.devs[dev_id_2]["region"])
                f.write(record)
                f.write("\n")
            elif ring_v1.devs[dev_id_1]["region"] ==ring_v2.devs[dev_id_2]["region"] and ring_v1.devs[dev_id_1]["id"]!=ring_v2.devs[dev_id_2]["id"]:
                local_migrate_count=local_migrate_count+1
            else:
                pass
        if region1_v1!=region1_v2:
            region_diff=region_diff+abs(region1_v1-region1_v2)

    f.write("local_migrate_num: "+str(local_migrate_count)+"\n")
    f.write("global_migrate_num: "+str(global_migrate_count)+"\n")
    f.write("region_diff is :" + str(region_diff))
    f.close()
    print "complete"

if __name__ == "__main__":
    count_migration()
