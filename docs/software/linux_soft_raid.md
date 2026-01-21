# Linux Soft RAID

- Examine state: `cat /proc/mdstat`, `sudo mdadm --detail /dev/md0`
- Remove RAID device: `sudo mdadm --stop /dev/md0`
- Create RAID0: `sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sda /dev/sdb`
- RAID device persistence (after assembling finished): `sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf`
- Import existing RAID: `sudo mdadm --assemble --scan`, `sudo mdadm --assemble /dev/md0 /dev/sda1 /dev/sdb1 /dev/sdc1`
- Replace failed drive: `sudo mdadm -–manage /dev/md0 -–remove /dev/sda1`, `sudo mdadm -–manage /dev/md2 -–add /dev/sdb1`

References:

- <https://www.digitalocean.com/community/tutorials/how-to-create-raid-arrays-with-mdadm-on-ubuntu>
