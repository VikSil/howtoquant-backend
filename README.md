# Release Notes

* Data fixes in marketdata MySQL seeding script
* Full dataset implemented in classifiers currency and country MySQL seeding scripts with 'active' flag
* Models added in accounting app
* My SQL seeding script for accounting app added
* Unified DB seeding script added
* Create and update date fields added to all models
* All endpoints refactored to return status and data fields
* Instrument type handling implemented for polygon.io instrument data download
* Minimum length restrictions added to API body validation schemas
* GET endpoints implemented for:
    * classifiers app: organization types, instrument classes, country names, currency ISO codes, industry sectors and subsectors, ticker types
     * staticdata app: organization by type, organization names by organization type,
     * accounting app: book, strategy, pb account
* POST endpoints implemented for:
     * staticdata app: organization, instrument
     * accounting app: book, strategy, pb account