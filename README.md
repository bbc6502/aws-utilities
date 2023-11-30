# AWS UTILITIES #

Utilities for AWS

## Installation ##

    pip install aws-utilities

## aws-assume-role ##

Assume an AWS role using the credentials in the specified profile

    $(aws-assume-role --profile default --role role_to_assume | grep export)
