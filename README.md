# AWS UTILITIES #

Utilities for AWS

## Installation ##

    pip3 install --upgrade https://github.com/bbc6502/aws-utilities/archive/refs/heads/main.zip

## aws-assume-role ##

Assume an AWS role using the credentials in the specified profile

    $(aws-assume-role --profile default --role role_to_assume | grep export)
