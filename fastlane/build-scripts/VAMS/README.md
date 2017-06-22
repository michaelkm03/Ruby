# VAMS
VAMS support programs

## Stage Scripts

### Send to VIP

Sends a piece of content to the VIP Stage of a particular app.

Usage:
```
// Sends a piece of content to Victorians (appID 24) in Staging
$ python send_to_vip.py --contentID 24198596 

// Sends a piece of content to Braindex (appID 1) in Staging
$ python send_to_vip.py --contentID 11198596 --appID 1 

// Sends a piece of content to Braindex (appID 1) in dev
$ python send_to_vip.py --contentID 11198596 --appID 1 --environment dev 
```

| Parameter | Type | Description | Required? | Default |
| :-------- | :--- | :---------- | :-------- | :------ |
| `contentID` | Integer | The content id of the content to send to the VIP Stage. | Yes | N/A |
| `appID` | Integer | The app id of the content to send to the VIP Stage. | Yes | `24`(Victorians) |
| `environment` | `dev` \| `staging` \| `production` | The content id of the content to send to the VIP Stage. | Yes | `staging` |

### Create Show

Usage:
```
// Creates a new show in Victorians (appID 24) in staging with the name "This is a show".
python create_show.py --showName "This is a show"


// Creates a new show in Braindex (appID 1) in staging with the name "This is a show".
python create_show.py --showName "This is a show" --appID 1


// Creates a new show in appID 11 in staging with the name "This is a show".
python create_show.py --appID 11 --environment staging --showName "This is a show"
```

Creates a show in a given APP ID & Environment.

| Parameter | Type | Description | Required? | Default |
| :-------- | :--- | :---------- | :-------- | :------ |
| `showName` | Integer | The name of the show that is being created. | Yes | N/A |
| `appID` | Integer | The app id of the show. | Yes | `24`(Victorians) |
| `environment` | `dev` \| `staging` \| `production` | The content id of the show. | Yes | `staging` |

### Update Show

Usage:
```
// Updates the playlist for a show with id 1 from the given file "example.csv"
python update_show.py --showID 1 --file example.csv

// Updates the playlist for a show with id 1 from the given file "example.csv" in Braindex (appID 1)
python update_show.py --showID 1 --file example.csv --appID 1

// Updates the playlist for a show with id 1 from the given file "example.csv" in Victorians (appID 11) in staging
python update_show.py --showID 1 --file example.csv --appID 11 --environment staging
```

Updates a given show with a new playlist from a `.csv` file.

| Parameter | Type | Description | Required? | Default |
| :-------- | :--- | :---------- | :-------- | :------ |
| `file` | File(`.csv`) | The file to use for the playlist of the show. | Yes | N/A |
| `showID` | Integer | The show id of the show that is being updated. | Yes | N/A |
| `appID` | Integer | The app id of the show. | Yes | `24`(Victorians) |
| `environment` | `dev` \| `staging` \| `production` | The content id of the content to send to the VIP Stage. | Yes | `staging` |

The `.csv` file should be formatted with the following format:
* Use the comma character `,` as the delimeter. No spaces
* Table header at the top with contentID, and duration to indicate the columns. No spaces
* Each row should first have the contentID, then the duration for which that piece of content should be on stage for. No spaces

Example:
```
contentID,duration
1001,1
1002,2
1003,3
```
This file would result in a show of 3 items with ids: `1001, 1002, 1003` that play for 1, 2, and 3 seconds respectively.


### Schedule Show

Usage:
```
// Schedules a show with show ID 2 on the main stage in Victorians(appID 24) on Production immediately.
python schedule_show.py --showID 2

// Schedules a show with show ID 2 on the vip stage in Victorians(appID 24) on Production immediately.
python schedule_show.py --showID 2 --stage vip

// Schedules a show with show ID 2 on the main stage in Braindex(appID 1) on Production immediately.
python schedule_show.py --showID 2 --stage main --appID 1

// Schedules a show with show ID 2 on the main stage in Victorians(appID 24) on dev immediately.
python schedule_show.py --showID 2 --stage main --appID 11 --environment dev

// Schedules a show with show ID 2 on the main stage in Victorians(appID 24) on Production in 5 seconds.
python schedule_show.py --showID 2 --startOffset 5
```

Schedules a given show to a particular stage.

| Parameter | Type | Description | Required? | Default |
| :-------- | :--- | :---------- | :-------- | :------ |
| `showID` | Integer | The show id of the show that is being updated. | Yes | N/A |
| `appID` | Integer | The app id of the show. | No | `24`(Victorians) |
| `environment` | `dev` \| `staging` \| `production` | The content id of the content to send to the VIP Stage. | No | `staging` |
| `stage` | String | The stage to schedule to. Can be either 'main' or 'vip'. | No | 'main' |
| `startOffset` | Integer | A start offset from now to schedule an item to the timeline. | No | 0 (schedule now) |

