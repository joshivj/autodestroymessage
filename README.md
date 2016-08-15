# Auto Destroy Message
- Auto Destroy Message after Reading

## Features
* Creates Encrypted Messages.
* Unique hashed URL is provided on message creation this can be communicated to other user.
* The message self destroy itself after reading from the user side.
* Even if DB security is compromised, no-one will be able to access the message which is send to other user as everything is encrypted.
* When the message is read, we deletes the message and save the IP address of the user and the time of reading the note.
* Bootstrap UI is provided.
