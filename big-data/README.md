# Big Data Reading Notes

## Chapter 1

- Traditional systems have failed to sale to Big Data
- A new breed of technologies have emerged to tackle the Big Data problem
- The new approach for the Big Data paradigm is dubbed "Lambda Architecture"
- Using Queues as a buffer between system components enables flexibility
- Sharding is used to scale databases that are write-heavy and have reached
  their single server limitations.
- The following are important issues to consider when Sharding:
    - Fault-tolerance
    - Corruption
    - As system complexity increases, so does the chance of human error
    - Maintenance is a lot of work
- Storing immutable data provides insurance against human error
- "A data system answers questions based on information that was acquired in the
  past."
- Any query can be answered by running a function on the complete dataset
- You will **not** always use the exact same technologies every time you
  implement a data system
- Systems need to behave correctly in the face of machines going down randomly
- Scalability is the ability to maintain performance in the face of increasing
  data and/or load by adding resources to the system
- An important part of minimizing maintenance is choosing components that have
  as small an implementation complexity as possible
- A trick employed in the Lambda Architecture is to push complexity out of the
  core components and into pieces of the system whose outputs are discardable
  after a few hours
- Lambda Architecture is composed of 3 high level layers:
    - Speed layer
    - Serving layer
    - Batch layer
- Batch layer processes and creates a precomputed, batch view of the raw data
- Serving layer provides functions that load the batch views so they can be
  queried
- Speed layer resolves queries by getting results from both the batch and real
  time views and merging them together
- Complexity isolation is when complexity is pushed into a layer whose results
  are only temporary

## Chapter 2
