[![Build Status](https://travis-ci.org/edbrannin/contacts.svg?branch=master)](https://travis-ci.org/edbrannin/contacts)

## Setup

1. Create `instance/config.py` with the following values:
    * `FACEBOOK_APP_ID`
    * `FACEBOOK_APP_SECRET`
    * `ALLOWED_USERS` (a list of email addresses)
    * `SECRET_KEY`

## Requirements

Ted says:

> I talked it over with David, and our business rules are about the same as they were for the original contacts list. In brief:
>
> 1. Secure authentication.
> 2. Display all contact information in a table on one page. (This allows for in-browser searching, which is more than good enough for our purposes.)
> 3. Organize contacts into different groups using tags; display all contact information from a given group in a table on one page.
> 4. Add, remove, and edit contacts and contact information. (The “Notes” field has been especially helpful.)
> 5. Sort on different columns, especially last name and zip code. (I implemented this client side using a JavaScript library, which has worked just fine.)
> 6. Generate mailing labels for a given group in PDF.
>
> If you set something like this up in Python and gave me a brief orientation on how it operates, I could do a lot in the way of maintenance and troubleshooting. (I’ve done some work in Python, so I wouldn’t be as out-to-sea as I was on the Ruby contacts list.)

Also:

> You can probably drop "active," "verified," and "added" from the main table view. We never used those much. (Might have done if there had been a "set to today" button.)


I'm just adding this sentence to check if it winds up in the container.

## Other considerations

* https://geemus.gitbooks.io/http-api-design/content/en/index.html
* [API Error format](https://dev.to/suhas_chatekar/return-well-formed-error-responses-from-your-rest-apis)
    * https://geemus.gitbooks.io/http-api-design/content/en/responses/generate-structured-errors.html

## Roadmap

### Release 1 (DONE)

- Read-only
- [x] List all contacts
- [x] Show contact details (no tags)

### Release 2

- [x] Edit contact details
- [x] List contacts by tag
- [x] Edit (Audit) log for contacts

### Release 3

- [x] Show tags for contact
- [x] Edit contact tags

### Release 4

- [x] Add contact (and tags)

### Release 5

- [x] Render Address Label PDF of current tag-view
    - https://pypi.python.org/pypi/pylabels/1.0.0

### Release 6

- [ ] UI for PDF printing
- [ ] Fix Create Contact

### Later

- [ ] Edit-log Automagic (via before-commit hook)?
- [ ] Better error display for AJAX (in dev?)?
- [ ] JSON-API?
- [ ] Add/remove/rename tags
- [ ] Merge tags
- [ ] Show (And sort by?) contacts-per-tag 
    - https://stackoverflow.com/questions/25500904/counting-relationships-in-sqlalchemy
    - https://stackoverflow.com/questions/19484059/sqlalchemy-query-for-object-with-count-of-relationship

## By Component

### Model

* [x] Add a person
* [x] Select all people
* [x] Select all people with one tag
* [x] ...with any number of tags
* [x] Edit a person's details
* [x] Edit a person's tags
* [ ] (Soft?) delete a person
* [ ] Sort by columns (last name, zip code, etc) (in-browser?)

### API

* [x] Facebook auth
    * [x] Block unathorized access
    * [x] ... accepting only pre-configured accounts
    * [x] Log out
* [x] Add a person
* [x] Select all people
* [x] Select all people with one tag
* [x] ...with any number of tags
* [x] Edit a person's details
* [ ] (Soft?) delete a person
* [ ] Sort by columns (last name, zip code, etc)
* [x] Generate a PDF of mailing labels for a given tag's people
    * Tag URL (right-click, copy) + `.pdf`

### UI

* [x] Facebook auth
    * [x] Block unathorized access
    * [x] ... accepting only pre-configured accounts
    * [x] Log out
* [x] Add a person
* [x] Select all people
* [x] Select all people with one tag
* [ ] ...with any number of tags
* [x] Edit a person's details
* [x] Edit a person's tags
* [ ] (Soft?) delete a person
* [ ] Sort by columns (last name, zip code, etc)
* [ ] Generate a PDF of mailing labels for a given tag's people
* [ ] Hide phones unless clicked(?) (for privacy reasons)

### Future

* DB-configurable user whitelist
    * Currently config-file
* Event-log-driven data migration
    * http://eventsourcing.readthedocs.io/en/v3.1.0/topics/domainmodel.html

