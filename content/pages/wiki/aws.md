Title: AWS
Status: Hidden

# Using an EventSourceMapping to feed Kinesis records into a Lambda function

* The ESM calls the Lambda function _synchronously_
    - Pitfall: A DLQ configured on the Lambda function itself only applies to
      _asynchronous_ invocations. Need to configure the DLQ as an [on-failure destination on
      the
      ESM](https://aws.amazon.com/blogs/compute/new-aws-lambda-controls-for-stream-processing-and-asynchronous-invocations/)
* If retries are not configured on the ESM, the default behavior is to retry
  until the records on the data stream expire
* Retries are literally what it sounds like: retries in addition to the initial
  attempt
    - So, X retries means a total of X+1 attempts
    - It's easy to conflate the `MaximumRetryAttempts` on the ESM with the
      `maxReceiveCount` attribute on SQS, where X maximum receives means X total
      attempts
