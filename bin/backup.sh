#!/bin/bash

print_help() {
    echo "Usage: $0 -s <source> -d <dest> [-p <previous_backup>]"
}

while [ $# -gt 0 ]
do
    case $1
        in
        -s)
            SOURCE=$2
            shift 2
            ;;
        -d)
            DESTINATION=$2
            shift 2
            ;;
        -p)
            PREVIOUS=$2
            shift 2
            ;;
        *)
            echo "Unknown arg $1"
            print_help;
            exit 1
    esac
done

if [[ -z $SOURCE ]]; then
    print_help
    exit 1
fi

if [[ -z $DESTINATION ]]; then
    print_help
    exit 1
fi

if [[ -n "$PREVIOUS" ]]; then
    LINK=--link-dest=$PREVIOUS
fi

date=`date "+%Y-%m-%dT%H_%M_%S"`

START=$(date +%s)
rsync -aAXP \
    --delete \
    --delete-excluded \
    --exclude={/dev/*,/proc/*,/sys/*,/tmp/*,/run/*,/mnt/*,/media/*,/lost+found,/home/lost+found} \
    $LINK \
    $SOURCE \
    $DESTINATION/incomplete_backup_$date && \
    mv $DESTINATION/incomplete_backup_$date $DESTINATION/$date
FINISH=$(date +%s)
echo "total time: $(( ($FINISH-$START) / 60 )) minutes, $(( ($FINISH-$START) % 60 )) seconds"
