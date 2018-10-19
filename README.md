Mavenlink
----------

A simple cli to help you work with mavenlink and provides a series of importers



## Usage

### Story 1 - Configure

As an user
I need to configure my mavenlink connection
So that I can inject **timesheets** 

`mavenlink setup /path/to/project/dir|.`

* will create a `.mavenlink.yml` file with default config for you to complete

### Story 2 - Show Config

As an user
I need to preview my config
So that I can send the right **timesheet** 

`mavenlink config`

* will preview the current `.mavenlink.yml` settings


### Story 3 - Obtain Oauth Token

As an user
I need to complete the oauth2 auth process to obtain a bearer token
So that I can send data to mavenlink

`mavenlink login`

* will use the `config.auth` data to request a token from mavenlink


### Story 4 - Consume Timesheets

As an user
I need to consume data from an input source
So that I can prepare a json object to send to mavenlink

`mavenlink consume :processor stdin`

* will allow the user to specifiy a `:processor` (json|csv|yaml)


### Story 5 - Preview Timesheet

As an user
Who has just consumed their timesheet data
I need to preview the timesheets I am about to send to mavenlink

`mavenlink preview`

* will output a preview of the data about to be sent


### Story 6 - Submit timesheet

As an infra-op
I need to create a new environment, optionally excluding or including certain modules
So that I can inject goodness into the lives of our clients

`mavenlink send`

* will send the prepared timesheet to mavenlink



## Development

``` bash
docker build -t mavenlink:latest .
docker run -it --rm \
       -v $PWD:/src \
       -v /Users/ross/p/ross.crawford/ti-landscape:/terraform \
       mavenlink:latest sh

docker run -it --rm \
       -v $PWD:/src \
       mavenlink:latest sh
```

## Using

``` bash
docker run -it --rm \
       -v $PWD:/src \
       -v /path/to/project:/terraform \
       rosscdh/mavenlink:latest sh

>> mavenlink setup /terraform
>> ls /tearraform
```