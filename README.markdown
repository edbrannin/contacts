[![Build Status](https://travis-ci.org/edbrannin/contacts.svg?branch=master)](https://travis-ci.org/edbrannin/contacts)

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

- [ ] Edit-log Automagic (via before-commit hook)
- [ ] Show tags for contact
- [ ] Edit contact tags

### Release 4

- [ ] Add contact (and tags)

### Release 5

- [ ] Render Address Label PDF of current tag-view

## By Component

### Model

* [x] Add a person
* [x] Select all people
* [x] Select all people with one tag
* [x] ...with any number of tags
* [x] Edit a person's details
* [ ] Edit a person's tags
* [ ] (Soft?) delete a person
* [ ] Sort by columns (last name, zip code, etc) (in-browser?)

### API

* [x] Facebook auth
    * [x] Block unathorized access
    * [x] ... accepting only pre-configured accounts
    * [x] Log out
* [ ] Add a person
* [x] Select all people
* [x] Select all people with one tag
* [x] ...with any number of tags
* [x] Edit a person's details
* [ ] (Soft?) delete a person
* [ ] Sort by columns (last name, zip code, etc)
* [ ] Generate a PDF of mailing labels for a given set of people

### UI

* [x] Facebook auth
    * [x] Block unathorized access
    * [x] ... accepting only pre-configured accounts
    * [x] Log out
* [ ] Add a person
* [x] Select all people
* [x] Select all people with one tag
* [ ] ...with any number of tags
* [x] Edit a person's details
* [ ] Edit a person's tags
* [ ] (Soft?) delete a person
* [ ] Sort by columns (last name, zip code, etc)
* [ ] Generate a PDF of mailing labels for a given set of people
* [ ] Hide phones unless clicked(?) (for privacy reasons)

### Future

* DB-configurable user whitelist
    * Currently config-file
* Event-log-driven data migration

