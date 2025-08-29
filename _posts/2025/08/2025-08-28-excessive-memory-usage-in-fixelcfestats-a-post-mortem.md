---
layout: post
title: 'Excessive memory usage in fixelcfestats: a post mortem'
author: 'Lestropie'
date: 2025-08-28 12:12:31
categories:
summary: posted by Robert Smith on Aug 28, 2025
---
# Excessive memory usage in `fixelcfestats`: a *post mortem*

This is a long overdue post relating to the computational performance of `fixelcfestats`, specifically in circumstances where the number of input fixel data files is very large. Apologies to those involved, and any others whom may have been affected, for taking so long to report back on this. I will elsewhere be writing a separate piece relating to my absence from this forum and its relationship to my incapacity to resolve many such issues more promptly. Here I'll be focusing exclusively on the story of `fixelcfestats`'s excessive RAM usage.

It's a long story, so zero judgement for anyone who puts this in the TL;DR basket, but I'd prefer for the whole thing to be publicly visible. I'm also hoping that it might provide some insight into how we think about research software engineering problems, even if one can't fully grasp the relevant code snippets.

## First awareness of issue

My first encounter with this particular issue occurred upon receiving *an invitation to review the manuscript* entitled:
"ModelArray: a memory-efficient R package for statistical analysis of fixel data"
([Preprint](https://www.biorxiv.org/content/10.1101/2022.07.12.499631v1.full)).

There they reported an inability to perform fixel-based statistical inference using `fixelcfestats` due to the RAM usage being highly excessive when using a combination of a very large number of input fixel data files (around 1,000 in their desired use case) and extensive multi-threading.

![Screenshot from 2025-08-28 21-18-43|531x414](upload://suqetQ5kmqN11UHZ6x8sVqAsohv.png)

This motivated the creation of an alternative software package for inference of fixel-based measures that was specifically designed for the minimisation of memory usage:
[ModelArray](https://github.com/PennLINC/ModelArray).

Apologies to those authors if there had been any earlier attempt to contact me regarding this excessive memory usage prior to the creation of their software or the writing of this manuscript; a *lot* has slipped through the cracks in the pat few years.

In the interest of full transparency, I will state to all openly here:

**I accepted this review invitation, identified myself to the authors, and explained the situation to the editor.**

I hope that the authors are content with the state of their final article incorporating my feedback, [published in NeuroImage](https://www.sciencedirect.com/science/article/pii/S1053811923001830). I further hope that the following content of this post will provide more robust justification for some of the recommendations I made during that process, making up some small fraction for my inability to provide an exhaustive diagnosis at the time.

## Basic operation of the statistical inference pipeline

I'm going to try to give a lay description of how the relevant code works, so that regardless of a reader's familiarity with software code, the story here has a chance of making sense.

1.  All input fixel data are explicitly loaded from the various fixel data files that are specified as the input file list, into a single large 2D matrix of numerical data, with the numbers of rows and columns in that matrix corresponding to the numbers of input files and fixels respectively.

2.  The General Linear Model (GLM) is responsible for deriving, given the input data, design matrix, and contrast of interest, a "test statistic" for each fixel.
    
    This runs independently across multiple threads. Each thread processes an individual *shuffling* of the input data. Multiple threads may read from the same input data at the same time, but this does not cause any issues with race conditions.
    
3.  The Connectivity-based Fixel Enhancement (CFE) method takes as input the test statistics as computed by the GLM, and "enhances" these values by looking for fixels that both exhibit large test statistics and are highly connected to one another.
    
    This step also runs in a wholly multi-threaded manner. Each thread takes as input a matrix of test statistics produced by the GLM: here, the number of rows is equal to the number of fixels, and each column corresponds to a specific *hypothesis* (since multiple hypotheses can be tested with a single command invocation).
    
    The other requisite input data in the case of `fixelcfestats` is the fixel-fixel connectivity matrix. From version 3.0.0, this matrix is pre-computed using the `fixelconnectivity` command and provided as one of the inputs to `fixelcfestats`: https://github.com/MRtrix3/mrtrix3/pull/1543

4.  Data from across the various threads must be aggregated to form one or more non-parametric null distributions.

5.  Once generation of the null distributions(s) is completed, data produced from the GLM in step 2, but *without* any random shuffling applied, and enhanced using CFE in step 3, are compared to the non-parametric null distributions produced in step 4 to produce a FWE-corrected *p*-value for each fixel.

![Screenshot from 2025-08-28 18-06-01|689x388](upload://t2zf08lF57B11PWqXFtBc9zGH0g.png)

## Diagnosis of the problem

Instinctively, there is no intrinsic reason why performing fixel-based statistical inference should become computationally infeasible from the perspective of dynamic memory allocation merely because the number of input fixel data files is large.

### *a priori* expectations

Regarding the components of the framework as described above:

1.  The input data are stored as a single 2D matrix and are deliberately *not* duplicated across multiple threads. The memory consumed for the storage of the input data should therefore *not* scale with the number of executing threads if the implementation is behaving as intended. I was therefore confident that this would not be a source of the problem.
    
    While the total memory consumption of the command could be reduced by storing and accessing the input data in such a way that does not require an explicit load of all input data into RAM (and the ModelArray authors demonstrate how to do so), *not* doing so was an explicit design decision in *MRtrix3*. I discuss this in more detail in "Speculative changes to further reduce memory" below.
    
2.  The General Linear Model (GLM) code underwent *extensive* changes for the 3.0.0 production release, providing myriad enhanced capabilities:
    https://github.com/MRtrix3/mrtrix3/pull/1543
    
![Screenshot from 2025-08-28 16-12-07|690x436](upload://ldRiwMteCNNAXutWUqRthcLxv9K.png)

    This was therefore my leading hypothesis for the source of excessive memory usage; though as will be shown further below, it required greater inspection than I afforded to the issue at the time.
    
3.  While the fixel-fixel connectivity matrix utilised by CFE is quite large in size, it was not expected to be the source of this problem for several reasons:
    
    1.  This matrix is immutable. It should therefore not need to be duplicated across multiple execution threads.
    
    2.  The total size of the fixel-fixel connectivity matrix in the form in which it is stored on disk is *smaller in size* than what is required to first generate it using the `fixelconnectivity` command. `fixelconnectivity` by default applies a threshold to remove very weak fixel-fixel connectivity connections prior to writing to disk; but this obviously can only be determined upon formation of the complete matrix containing all non-zero connections. As such, if, for a given fixel dataset and template tractogram, a user was capable of generating the fixel-fixel connectivity matrix (which was known to be the case in this instance during the review process given that fixel data smoothing was reported to have been performed), then it would be entirely expected that the size of that matrix should *not* be prohibitive further downstream the analysis pipeline.
    
    3.  Because of the way in which the fixel-fixel connectivity matrix is stored on the filesystem and accessed, it should be possible for that matrix data to be accessed using *memory-mapping*, avoiding an explicit load of all such data into RAM and therefore not incurring prohibitive memory consumption.
    
4.  Creation of the null distribution(s) should not scale with the number of threads. Writing the data for the null distribution(s) is done in a thread-safe manner by pre-allocating the memory to store the entire null distribution(s), and for each individual shuffling of the data, finding the maximal value of the test statistic across all fixels, and writing that value into the right position in the null distribution according to the unique index assigned to that particular shuffle. This ensures that there are never two threads trying to write to the exact same item in memory: each only writes to those elements in the null distribution(s) corresponding to the shuffles that it is responsible for processing. This should therefore not be the source of reported excessive RAM usage. While the amount of memory can scale according to the number of hypothesis tests, the authors' use case did not involve such testing, and the size required for such data is a drop in the pan compared to other aspects of the pipeline.
    
### Measurement of memory usage

The ModelArray authors exemplify use of a software tool dedicated to the measurement of memory usage of software commands (which is not as trivial as one might naively imagine):
[https://www.brendangregg.com/wss.html](https://www.brendangregg.com/wss.html).

I was not previously aware of this particular tool, and adopt it throughout my investigation below.
    
### Reproduction    
    
I had a reasonable hypothesis that the excessive memory consumption was due to the internal operation of the new General Linear Model implementation, and would have nothing to do with the specifics of handling of fixel data within the `fixelcfestats` command. I therefore instead focused my efforts on the `vectorstats` command. This operates in a very similar way to the `connectomestats`, `mrclusterstats` and `fixelcfestats` commands, except that it takes as input *structureless* numerical data. The consequence to the absence of structure within such data is that no statistical enhancement can be performed; but the statistical framework is otherwise identical. The name "`vectorstats`" arises from the fact that the input to this command is a text file containing a list of file names just as with other *MRtrix3* statistical inference commands, but each of those files contains simply a 1D vector of numerical data.

I rigged up a Python script that would generate for me random data in the correct form to feed them into `vectorstats`. I used 1000 inputs, similar to the size of the cohort in use by the authors, and chose 500,000 fixels as a typical size for FOD templates.

To begin, let's look at the 3.0.x version of the software:

| `-nthreads` | Time (m) |  RSS (MB) |
|-------------|----------|-----------|
|           0 |      697 |     15411 |
|           1 |      673 |     16193 |
|           2 |      370 |     23877 |
|           3 |      256 |     31563 |
|           4 |      194 |     39246 |

So the increase in RAM usage with an increasing number of threads is clearly visible. It doesn't scale in direct proportion to the number of threads: it looks like there's maybe 8GB of fixed usage, plus another 8GB for each processing thread. 
    
Note here that I've deliberately disambiguated between the use cases of `-nthreads 0` and `-nthreads 1`:

-   For `-nthreads 0`, the multithreading-safe data queue structure demonstrated diagrammatically in  [Figure 3 of the MRtrix3 NeuroImage manuscript](https://www.sciencedirect.com/science/article/pii/S1053811919307281#fig3) is [*never even instantiated*](https://github.com/MRtrix3/mrtrix3/blob/3.0.7/core/thread_queue.h#L1056-L1062). The code responsible for the various operations---in this case the generation of shuffles and the imposition of the GLM---operates in a strictly sequential fashion, generating and then processing each shuffle in order.
    
-   For `-nthreads 1`, the full multi-threading queue is set up, which consists of a single thread responsible for the generation of random shuffles and writing these to a queue, and multiple threads that read shuffles from this queue and process them. The way that this specific invocation is interpreted is: "For the component of a multi-threading pipeline that is multi-threaded, instantiate 1 thread". This is why it doesn't yield any particular performance benefit: in both cases there is only one thread doing the heavy lifting in terms of fitting the GLM and deriving test statistics for each shuffle.
    
### Had the problem already been fixed?    
    
A key concern of mine when performing the journal review, which I expressed to the authors at the time, was that the excessive memory usage observed for `fixelcfestats` may have been not only an outright *bug* (which would therefore limit motivation for an alternative implementation as opposed to simply fixing the bug), but indeed may have *already been fixed*, only that said fix was not yet integrated into a tagged release of the software. I provided a link to the following Pull Request: [https://github.com/MRtrix3/mrtrix3/pull/2269](https://github.com/MRtrix3/mrtrix3/pull/2269)

I had previously independently observed, through crude observation of the output of the `top` command, that the reported memory consumption of `fixelcfestats` would often fluctuate markedly. This I hypothesised was the result of sub-optimal structure of the code class responsible for fitting the GLM in the 3.0.x version of the software. I'm going to show some C++ code here to make the point, but I'll simplify as much as I can, and explain the relevant parts in such a way that those not familiar with the language can still gain insight.

In [header file `core/math/stats/glm.h`](https://github.com/MRtrix3/mrtrix3/blob/3.0.7/core/math/stats/glm.h), the [following class is defined](https://github.com/MRtrix3/mrtrix3/blob/3.0.7/core/math/stats/glm.h#L273-L300):

```cpp
// 01-01. Declaration of the class structure
class TestFixedHomoscedastic : public TestBase
{
    // 01-02. "Functor" function declaration;
    //        this is just the interface to the function, not its content
    void operator() (const matrix_type& shuffling_matrix, matrix_type& stats, matrix_type& zstats) const override;

    // 01-03. Data that doesn't change each time the input is shuffled,
    //        and can therefore be precomputed and stored
    vector<Hypothesis::Partition> partitions;
    const matrix_type pinvM;
    const matrix_type Rm;
    vector<matrix_type> XtX;
    vector<default_type> one_over_dof;

};
```

The name "`TestFixedHomoscedastic`" is in reference to the fact that within *MRtrix3* there is currently not one class responsible for fitting the GLM, but *four*; which is used depends on the input data and/or features of the model as specified by the user. I expand further on this later in the article in the "Per-fixel design matrices" section; for now just consider this as "the class responsible for the GLM".

Corresponding source code file [`core/math/stats/glm.cpp`](https://github.com/MRtrix3/mrtrix3/blob/3.0.7/core/math/stats/glm.cpp) then provides the [definition of the function shown above](https://github.com/MRtrix3/mrtrix3/blob/3.0.7/core/math/stats/glm.cpp#L583-L662):

```cpp
// 01-04. The interface of the function;
//        note this is the same as the declaration in the header file shown above,
//        but here the code within the function will actually be shown
void TestFixedHomoscedastic::operator() (const matrix_type& shuffling_matrix,
                                         matrix_type& stats,
                                         matrix_type& zstats) const
{
    // 01-05. Pre-define some data that we will be computing
    matrix_type Sy, lambdas, residuals, beta;
    vector_type sse;

    // 01-06. Loop over the set of hypotheses being tested
    for (size_t ih = 0; ih != c.size(); ++ih) {

        // 01-07. Compute residuals from fitting reduced model to data y, and shuffle them
        Sy = shuffling_matrix * partitions[ih].Rz * y;

        /* 01-08. Compute other global features of the GLM for this shuffle */

        // 01-09. Loop over "elements" (fixels in the case of fixelcfestats)
        for (size_t ie = 0; ie != num_elements(); ++ie) {
        
            /* 01-10.  Do per-fixel operations */ 

        }
    }   
}
```

This function takes as *input* the *shuffling matrix* that defines one specific random shuffling of the input data to be used during generation of the null distribution, and writes as its *output* the computed test statistics (with size depending on the number of fixels and number of hypotheses). *Two* different data structures are written:

1.  The test statistic native to that hypothesis (either a *t*-statistic or *F*-statistic in the case of this particular class);
    
2.  The respective Z-transform of each of those statistics. From 3.0.0 it is not actually the *t*-value or *F*-value that undergoes statistical enhancement, but the Z-transformed versions of such, since this better standardises the behaviour of statistical enhancement across experiments.

This function is therefore executed as many times as there are unique shuffles of the data (default: 5000).

I had previously hypothesized that what was causing my observation of oscillation in total memory usage was that the set of data objects defined at step number 1. above was being *allocated* when the function was run for a given shuffle, then *released* upon completion of processing of that shuffle, only to then be *re-allocated* upon commencement of processing of the next shuffle. This should not be necessary, and probably arose due to the effort required to get all four GLM classes operating as required.

As such, prior to receive the journal review invitation, I had already modified this code within a feature branch, investing greater effort into recognising what data were both amenable to pre-computation and shared between GLM classes, and preventing repeated reallocation of data. Here is [the corresponding section of the header file at the time at which this review took place](https://github.com/MRtrix3/mrtrix3/blob/e1546a5d27268abc01f7359b8e2e47aa9e047d7b/core/math/stats/glm.h#L318-L369):

```cpp
// 02-01. Updated definition of the GLM test class
class TestFixedHomoscedastic : public TestBase
{
    // 02-02. A class that encompasses all of the data that can be shared across GLM threads
    class Shared
    {
        
        /* 02-03. Other features of this Shared class */
        
        // 02-04. The data that is pre-computed and stored within this Shared class;
        //        note correspondence to 01-03. above
        vector<matrix_type> XtX;
        vector<size_t> dof;
        vector<default_type> one_over_dof;
    };
    
    /* 02-05. Other features of the TestFixedHomoscedastic class */
    
    // 02-06. "Functor" function declaration; same as 01-02. above.
    void operator() (const matrix_type& shuffling_matrix, matrix_type& stats, matrix_type& zstats) override;

    // 02-07. Access to all of the data that is shared among threads
    const Shared& S() const;
    
    // 02-08. Data members of the TestFixedHomoscedastic class;
    //        note similarity to 01-05. above.
    matrix_type Sy, lambdas, residuals;
    vector<matrix_type> betas;
    vector_type sse;
};
```

There is one instance of this class created for every executing thread, regardless of the number of data shuffles that that thread processes. As such, the set of data variables originally defined in 01-05., which was being released upon completion of a shuffle only to be re-requested for the next shuffle, is instead requested only once for each thread in section 02-08. This should therefore result in greater stability in the reported memory consumption during execution of the command.

Here's the effect of this pre-existing change on the *range* of memory consumption as reported by the WSS tool, after having manually cropped the logging window to encompass only the period of time corresponding to the performing of data shuffling:

| Code branch | RSS minimum | RSS maximum |
|-------------|-------------|-------------|
| `master`    |        7753 |       15411 |
| PR#1543     |       23053 |       23053 |

Well, it's certainly *stabilised* the RAM usage, though it has also *increased* the total usage; I'll admit I've not exhaustively diagnosed this, but it should hopefully be shown to be irrelevant given later changes.

What I wasn't sure about at the time was whether the excessive memory usage reported in proportion to the number of executing threads would be rectified by this already-implemented change. Even with the original code, it *should* be the case that the operating system would have allocated to the process as much memory as required, such that de-allocating and re-allocating memory for those variables would simply be re-using that already allocated memory, not requiring any new memory requests to the operating system.

So, some three years late, here's what that code branch looks like running against my test data:

| `-nthreads` | Time (m) |  RSS (MB) |
|-------------|----------|-----------|
|           0 |      595 |     23053 |
|           1 |      624 |     23817 |
|           2 |      308 |     31503 |
|           3 |      221 |     39187 |
|           4 |      182 |     46870 |

Clearly the issue of increasing RAM usage as a function of thread count was *not* rectified by the changes that I had already made predating the journal review, and further interrogation was required.

### Testing hypothesised changes

What follows is the set of modifications to the implementation that I came up with and tried in the sequence in which they occurred.

#### 1. The shuffling matrices

The first idea that came to mind---even though i was reasonably confident that it would not ultimately be the primary source of excessive memory usage---was that the representation of the data shuffles was modified for version 3.0.0 in [Pull Request #1543](https://github.com/MRtrix3/mrtrix3/pull/1543).

Prior to this version, the only form of data shuffling that was available was *permutation*. Permutation can be efficiently encoded using a *list of integers*, encoding how to change the order of items in a list.

In 3.0.0 the ability to shuffle data through *sign-flipping* was introduced. The utility of this is explained in ([Winkler et al., 2014](http://www.sciencedirect.com/science/article/pii/S1053811914000913)). In isolation, this could be encoded as a *list of bits*, indicating for each input whether the sign should or should not be flipped for that shuffle. It is however also appropriate in certain experimental configurations to perform *both* of these forms of shuffling for generation of the null distribution. In this use case, if permutations and sign-flips were both to be encoded using these representations, then there may be a risk of erroneous implementation between the code responsible for *generating* these shuffles and that responsible for *applying* the shuffles, as the outcome would depend on the *order* in which these operations should be applied.

My chosen solution here was to store for each computed shuffle the full shuffling matrix to actually be applied to the data during the GLM computations. This is consistent with the description of the FSL `randomise` implementation, as described in the manuscript that acted as somewhat of a bible during my time implementing these advanced GLM capabilities:
"Permutation inference for the genreal linear model" 
[https://www.sciencedirect.com/science/article/pii/S1053811914000913](https://www.sciencedirect.com/science/article/pii/S1053811914000913).

This can however be expected to require more memory than the aforementioned encodings, is the size of that matrix scales with the *square* of the size of the input data.

I realised here that there were two ways in which I could reduce the RAM requirements here:

1.  Most floating-point calculations in *MRtrix3*, including those of statistical inference, are performed using double-precision floating-point: 64 bits, or 8 bytes, per value. These shuffling matrices however contain only the values -1, 0 and +1. This can be exploited to reduce the storage space required for these matrices. A signed 8-bit integer, which can only represent values between -128 and +127, is more than enough to encode all data present in these matrices. The Eigen library that we use for linear algebra in *MRtrix3* provides convenience functions that allow matrix data stored as one data type to be interpreted as another data type without necessitating an explicit bulk conversion of the whole data structure.
    
2.  When an *MRtrix3* command constructs a multi-threading processing pipeline that is based on non-image data, each of the multi-thread-safe queues in that pipeline will be constructed with a given *buffer size* to store some number of instances of whatever data class is passed from one class to another via that queue. This is done to maximise computational throughput regardless of whether it is the threads feeding data to the queue or reading from the queue that form the processing bottleneck. In this case however there is minimal benefit to storing large amounts of data in that buffer. It will be immediately populated with some number of large shuffling matrices much faster than the GLM can derive test statistics based on those shuffles. This buffer therefore likely only increases memory usage of the command without any counter-balancing improvement in computational speed.
    
These two changes are implemented in [commit d0b3afa83dbdf2fe711a865a64dcbab5d8325bc6](https://github.com/MRtrix3/mrtrix3/pull/2269/commits/d0b3afa83dbdf2fe711a865a64dcbab5d8325bc6), and yield:

| `-nthreads` | Time (m) |  RSS (MB) |
|-------------|----------|-----------|
|           0 |      619 |     19233 |
|           1 |      635 |     19252 |
|           2 |      318 |     26945 |
|           3 |      238 |     34637 |
|           4 |      182 |     42330 |

Compared to the original state of this Pull Request, this reduced the total memory utilisation across all thread counts, and also prevented the increase in memory required between requesting 0 threads vs. 1; this latter point will be the direct result of decreasing the size of the multi-thread-safe queue, as that queue is instantiated in the latter case but not the former.

#### 2. Matrix Blocks

At some point after finishing implementation of the changes above, contemplating the structure of the relevant GLM code, I had a flashback to the time I spent implementing these GLM enhancements, and immediately realised that I knew *exactly* where this behaviour of increasing RAM usage as a function of thread count was arising.

First, let's look at [the relevant section of code *prior* to 3.0.0](https://github.com/MRtrix3/mrtrix3/blob/3.0_RC3_last/core/math/stats/glm.cpp#L111-L135):

```cpp
// 03-01. The function that gets run once for each unique permutation
void GLMTTest::operator() (const vector<size_t>& perm_labelling, vector_type& stats) const
{

    // 03-02. Set up the intermediate and output data
    stats = vector_type::Zero (y.rows());
    matrix_type tvalues, betas, residuals, SX, pinvSX;

    /* 03-03. Construct the shuffling matrix for this permutation */
    
    // 03-04. Loop over all fixels in blocks
    for (ssize_t i = 0; i < y.rows(); i += GLM_BATCH_SIZE) {
    
        // 03-05. Grab the data for a subset of fixels
        const matrix_type tmp = y.block (i, 0, std::min (GLM_BATCH_SIZE, (int)(y.rows()-i)), y.cols());
          
        // 03-06. Do the actual GLM fitting
        GLM::ttest (tvalues, SX, pinvSX, tmp, scaled_contrasts, betas, residuals);
          
        /* 03-07. Write the results for this subset of fixels to the output */
        
    }
}
```

Note in particular sections 03-04. and 03-05 The simplest way to do this operation would be to simply loop over each fixel *individually*; for each fixel, apply the data shuffling, compute the test statistic, and save the result to the output data structure. What this code is instead doing is: for each iteration, grab data corresponding to a continguous *block* of fixels of some manageable size, perform the GLM fitting to all of the data within that block in a single step, and then insert the results from that block into the appropriate location in the output data structure. There's a little bit of gymnastics in 03-05. to make sure that, for the very last block of fixels, the size is reduced to accommodate however many fixels are left to be processed. This blocking is done because it allows the compiled program to make use of advanced features of modern CPUs exploited by the Eigen linear algebra library that maximise computational efficiency.

Now, however, look again at the 3.0.x code that was shown in code snippet 01 above:

```cpp
void TestFixedHomoscedastic::operator() (const matrix_type& shuffling_matrix,
                                         matrix_type& stats,
                                         matrix_type& zstats) const
{
    // 05-01. Data pre-allocation
    
    // 05-02. Looping over hypotheses
    for (size_t ih = 0; ih != c.size(); ++ih) {
    
        // 05-03. Compute the residuals from fitting the reduced model to data y, then shuffle them
        Sy = shuffling_matrix * partitions[ih].Rz * y;

        // ...

    }
}
```

Look at line 05-03. What this code is doing, is taking *all* of the input data `y`---all (n_fixels x n_inputs)---doing some calculations, and then storing a *new* shuffled version of those data. As such, while it's technically true that the code is *not* duplicating the *input* data for every executing thread, it *is* generating for each executing thread a 2D matrix of shuffled data, which has *exactly the same size* as the input data!

To reduce this memory burden therefore involves re-introducing the same block processing mechanism that was in use prior to version 3.0.0. This was implemented as part of [commit 592f4ce8cfedd414d1832091ef3de40939f90612](https://github.com/MRtrix3/mrtrix3/pull/2269/commits/592f4ce8cfedd414d1832091ef3de40939f90612) as part of [Pull Request #2269](https://github.com/MRtrix3/mrtrix3/pull/2269); the [most relevant block of code](https://github.com/MRtrix3/mrtrix3/pull/2269/commits/592f4ce8cfedd414d1832091ef3de40939f90612#diff-446d2526bdbac85f9a246a89ef6cf5c260066e301953005260677438e3bb46ffR711-R717) looks something like:

```cpp
    // 06-01. Loop over blocks of fixels
    for (index_type iestart = 0; iestart < num_elements(); iestart += batch_size()) {
    
        // 06-02. Determine number of fixels in this block
        //        (may be smaller than the nominated batch size for the last block)
        const index_type this_batch_size = std::min (num_elements() - iestart, batch_size());
        
        // 06-03. Do the model residual shuffling as before
        Sy.leftCols(this_batch_size) = shuffling_matrix * S().partitions[ih].Rz * y.block(0, iestart, num_inputs(), this_batch_size);
        
        /* 06-04. Proceed with the rest of the GLM computations */
    }
```

The code is more complex, as in many cases matrices of data are no longer just referred to by name, but must instead explicitly specify that it is some subset of data that is being operated on (there was obviously many more code changes to make this work, but this hopefully demonstrates the core of the change).

How does the memory usage of `fixelcfestats` look now?

| `-nthreads` | Time (m) |  RSS (MB) |
|-------------|----------|-----------|
|           0 |      879 |      7782 |
|           1 |      913 |      7797 |
|           2 |      483 |      7856 |
|           3 |      334 |      7916 |
|           4 |      257 |      7976 |

Bang.

Note however the runtime: in all cases, this code takes about 40% longer to execute. This I presume is due to the Eigen linear algebra library not being capable of generating machine code of the same efficiency for matrix operations in the scenario where it is operating not on entire matrix objects, but restricted subsets of matrix objects.

My *suspicion*, though I can't state such with certainty, is that when I was writing [Pull Request #1543](https://github.com/MRtrix3/mrtrix3/pull/1543) (the one that completely overhauled the GLM implementation), I determined that blocking was in fact *not necessary* for the scope of FBAs being done at the time, and was therefore not worth the code complexity or development time to re-establish that functionality. Indeed one might naturally intuit that a system capable of executing a large number of threads is likely to also corresponding possess a large amount of memory, thereby providing a natural mitigation. It seems however that attempting to run an FBA with 1,000 participants exceeded this naive heuristic.

#### 3. Single-precision data

While not strictly necessary given the change above, another idea nevertheless came to me as to how this memory usage could be decreased even further. As stated previously:

1.  All floating-point computations in *MRtrix3* where precision is important will be done using double precision.
    
2.  Using the Eigen linear algebra library, matrix data of one type can be cast on-the-fly to another type.
    
Consider therefore the input data to statistical inference. Throughout the various steps leading to the generation of fixel data files, image data will be stored as single-precision, 32-bit floating-point images. But given that all calculations performed within `fixelcfestats` are to be done in double-precision, the explicit load of all of those fixel data files into a single large 2D matrix is done using double-precision. Theoretically then, that data matrix could be modified to instead be stored as single-precision only, with the data cast to double-precision only when read.

This was implemented in [commit 97c1baa710645793d17307339e58d310c30a7264](https://github.com/MRtrix3/mrtrix3/pull/2269/commits/97c1baa710645793d17307339e58d310c30a7264) as part of [Pull Request #2269](https://github.com/MRtrix3/mrtrix3/pull/2269), and results in:

| `-nthreads` | Time (m) |  RSS (MB) |
|-------------|----------|-----------|
|           0 |      926 |      3971 |
|           1 |      889 |      3990 |
|           2 |      493 |      4050 |
|           3 |      327 |      4110 |
|           4 |      296 |      4171 |

Yep: as might have been expected, if most of the memory usage of the command is occupied by simply storing the input dataset, and you then halve the memory required to store each value in that dataset, then the overall memory usage of the command nearly halves. But as with the implementation of block operations in the GLM class, this could come with an execution time performance penalty.

### Speculative changes to further reduce memory

Within their work, the authors show how storing the input fixel data in an alternative data structure facilitates their software accessing those data without performing an explicit load of all data into RAM, thereby reducing the peak memory consumption requirements. Here I wish to comment on this specific prospect.
    
The *MRtrix3* statistical inference code performs an explicit load of all input data into RAM *despite* its existing capabilities elsewhere to avoid such explicit loading. Where possible, *MRtrix3* will use *memory-mapping* of image data, which allows the program to access data from a file on disk *as though* it had been loaded into RAM; the operating system deals with synchronisation between the block of RAM that it presents to the program as a view of the image data on disk and the actual data physically stored on the disk. The authors used precisely this technique to reduce the total RAM capacity required to run fixel-based statistical inference using their software.
        
This could *theoretically* be achieved in *MRtrix3* also. One could first concatenate all fixel data files along the second axis to produce a singular large 2D fixel data file, and modify the interface to the `fixelcfestats` command to take this file as input. I have however *not* invested the effort in doing so for several reasons:
        
1.  As shown in the relevant publication, the storage space required for the input data should not really be prohibitive even for very large datasets; a 1,000 participant cohort requires around 8GB, which is completely feasible for the kind of hardware one would expect to be utilising if processing such a cohort.
            
2.  As has been demonstrated here, storage of the complete dataset of all input fixel data is not the primary source of excessive memory usage in `fixelcfestats`. 
            
3.  The non-parametric statistical inference framework implemented in *MRtrix3* is shared across multiple commands that operate on fundamentally different forms of data (`connectomestats`, `fixelcfestats`, `mrclusterstats`, `vectorstats`; more to come in the future). The only way in which the internal operation of these commands differ is in the definition of the *statistical enhancement* algorithm that considers the expected covariance in the test statistics across the elements tested (in the case of `fixelcfestats`, this is the Connectivity-based Fixel Enhancement (CFE) method). This generalised implementation is *drastically simplified* by having all of these commands interface with the forms of their respective input data and collapse them into a 2D matrix of numerical data prior to feeding them through the statistical inference pipeline. That's not to say that a more memory-efficient implementation *isn't* possible; but keeping the implementation *simple* in this respect was an *explicit design choice* in *MRtrix3*.

### Was there an existing way to circumvent the problem?

Given knowledge of the origin of the excessive memory usage in `fixelcfestats`, we can now ask the question: might there have been an alternative usage of `fixelcfestats` that might have handled this large dataset given finite memory constraints without any modification of source code?

#### 1. Pre-3.0.0 `fixelcfestats`

The fixel statistical inference code underwent substantial changes in the 3.0.0 production release of the software, as shown by the size of [Pull Request #1543](https://github.com/MRtrix3/mrtrix3/pull/1543). This included:

1.  Addition of new command `fixelconnectivity`, which generates the fixel-fixel connectivity matrix and writes it to the file system. Command `fixelcfestats` then reads these data from the file system rather than itself generating the matrix and storing it in RAM; moreover, it should be capable of memory-mapping the images used to encode the fixel-fixel connectivity matrix, rather than explicitly loading the whole matrix into RAM.
    
2.  Reduction in storage size of the fixel-fixel connectivity matrix by approximately 80%, through better algorithmic & data structure design.
    
3.  Complete re-implementation of the GLM, though importantly here omitting the use of block operations for the most common use case as described above.
    
If we put all of these factors together, it is possible that for certain use cases, the total memory usage of `fixelcfestats` could actually be *smaller* for pre-3.0.0 code than it is for 3.0.x. This may seem counter-intuitive given point 2. above. But let's do some napkin math. From the tabular data shown above, for my synthetic use case intended to approximate that of the authors, there is about 8GB of RAM required per thread. We know from our history of writing the initial code for CFE that prior to these 3.0.0 enhancements, we had to build a system locally with 128GB of RAM; 64GB was not adequate given the choice of spatial resolution & tractogram density. So let's take the most pessimistic case, and assume that a pre-3.0.0 fixel-fixel connectivity matrix requires 128GB of RAM. Let's also assume that with 3.0.0 code, the fixel-fixel connectivity matrix can be memory-mapped, and therefore omit it from RAM requirement calculations. As soon as one runs `fixelcfestats` with more than ((128 - 8) / 8) = 15 threads, the 3.0.x version of the software may use more RAM than does the pre-production version.

#### 2. Per-fixel design matrices

Alongside code block 01 above, I stated that the name of the class responsible for fitting the GLM, "`TestFixedHomoscedasitc`", would be accepted as-is at that point in time, but the nuances would be explained later. Now is that time.

The one that is of relevance for this discussion is "`Fixed`". This isn't terribly informative on its own, and is not particularly clarified by its antonym class "`TestVariableHomoscedastic`". This relates to features of the *MRtrix3* GLM implementation that I am still yet to succeed in publishing despite being in place for many years.

What this terminology refers to is whether the GLM design matrix is *fixed* and consistent across every single fixel being tested, or whether the design matrix *varies* between fixels. There are two ways in which the design matrix might be different for two fixels despite those fixels being a part of the same statistical inference computations (which I promise I will try to publish and produce documentation for):

1.  *Exclusion* of input data on a per-fixel basis.

    There can be circumstances in which, for a given input fixel data source and a given template fixel, there is either no valid image data available, or the data available are for whatever reason deemed unreliable. In many such scenarios, encoding this as a quantitative value of 0.0 may not be suitable. Conversely, if one were exclude from their whole analysis any fixel for which there is just one participant where these criteria apply, one could end up with not being able to test their scientific hypothesis for those areas of the brain they wish to analyse. While one can do a certain amount of dataset curation to exclude subjects that have inadequate coverage of useful image data, this is not a panacea in all use cases.
    
    From version 3.0.0, this is handled by the use of the floating-point value "*Not-a-Number (NaN)*". Where the GLM reads the input data and sees this value, it removes the corresponding row of the design matrix prior to performing the regression to estimate the test statistic. This capability is exemplified in [this work](https://www.researchgate.net/publication/326146373_Mitigating_the_effects_of_imperfect_fixel_correspondence_in_Fixel-Based_Analysis), and [the software documentation contains instructions](https://mrtrix.readthedocs.io/en/3.0.7/fixel_based_analysis/mitigating_brain_cropping.html) for replicating that particular use case.
    
    NaNs can be inserted into one's data *at any point in an analysis pipeline*: any computation that attempts to make use of such data will itself yield a result of NaN, enabling the propagation of the characterisation of "no valid data available here" all the way through to the fixel data files in template space.
    
2.  Fixel-wise regressors

    There are circumstances in which an exploratory experimental variable that may have some influence on the input data to statistical inference, whether that influence is of key interest in some hypothesis test or a nuisance regressor, may itself not be constant for all fixels in template space. In this scenario, the data contained within the corresponding column of the design matrix will change as the GLM is fit to each fixel within the template. This capability was originally demonstrated [here](https://www.researchgate.net/publication/317357260_Toward_interrogating_relationships_between_grey_and_white_matter_measures_using_Fixel_Track-Weighted_Imaging_and_Fixel-Based_Analysis) looking at correlations between FDC and cortical thickness. There are *all sorts* of clever applications of this capability, which I'm hoping to describe in a publication in the near future.
    
In either of these cases, there are certain derivative calculations from the design matrix that can *no longer be pre-calculated*, since that design matrix is no longer immutable. Implementing these features into a singular GLM class, and having that class be utilised even in simpler FBA applications where such features are not actively utilised, could incur drastic computational performance penalties to the more common use cases, due to not maximally exploiting such pre-calculations. As such, I made the decision at the time to define *four* GLM classes, each computationally optimised to precompute as much as was applicable in that use case; the choice of which of these classes to instantiate depends on the input data and the user's invocation. That decision code can be seen [here](https://github.com/MRtrix3/mrtrix3/blob/3.0.7/cmd/fixelcfestats.cpp#L415-L427); as simplified pseudocode it looks something like:

```cpp
  if (extra_columns or nans_in_data) {
    if (have_variance_groups)
      /* Create TestVariableHeteroscedastic */
    else
      /* Create TestVariableHomoscedastic */
  } else {
    if (have_variance_groups)
      /* Create TestFixedHeteroscedastic */
    else
      /* Create TestFixedHomoscedastic */
  }
```

Now, why is this relevant to the context of this post? Well, when the GLM design matrix is different between different fixels, it becomes very difficult to process data from multiple fixels using block matrix operations that process multiple fixels at once. The math just ... doesn't math. So instead, if such features are necessary for a given experimental model, the fixels are processed *one at a time*. [Here's what that code looks like](https://github.com/MRtrix3/mrtrix3/blob/3.0.7/core/math/stats/glm.cpp#L849-L978):

```cpp
// 07-01. Definition of the functor:
//        note how the interface is the same as 01-04,
//        but here it is for the "TestVariableHomoscedastic" class rather than "TestFixedHomoscedastic"
void TestVariableHomoscedastic::operator() (const matrix_type& shuffling_matrix,
                                            matrix_type& stats,
                                            matrix_type& zstats) const
{
    /* 07-02. Pre-allocate memory for various data structures */

    // 07-03. Loop over fixels one at a time
    for (ssize_t ie = 0; ie != y.cols(); ++ie) {

        /* 07-04. Load any additional data and do other per-fixel calculations */

        // 07-05. Loop over hypotheses
        for (size_t ih = 0; ih != c.size(); ++ih) {

            /* 07-06. Calculate test statistic */

        }
    }
}
```

This code processes each fixel individually; the various data structures allocated in the omitted code at 07-02. only need to be large enough to store whatever is computed on a per-fixel basis. As such, the previous manifest excessive memory consumption, which occurs due to each thread generating a complete shuffled version of the whole input dataset, *should not happen here*.

I confirmed this by modifying my test code to insert a single NaN value in a single input file. `fixelcfestats` detects the presence of this NaN value, and correspondingly engages the `TestVariableHomoscedastic` class as per the code snippet above. Here's the result of execution:

| NaN present | `-nthreads` | Time (m) |  RSS (MB) |
|-------------|-------------|----------|-----------|
|          No |           4 |      194 |     39246 |
|         Yes |           4 |    92719 |      8825 |

The RAM usage remains low despite use of multiple threads as expected.

The execution time is however fairly impractical in this scenario. This could possibly be improved with justifiable investment in software development. For instance, imagine that the code could look across the fixel dataset, identify the fact that there are only two unique applicable design matrix---one including all input data and one excluding just one input---and perform the respective GLM pre-calculations for those two cases; as multiple threads are then processing fixels across the large number of shuffles, they could access for each fixel the appropriate pre-calculated data. This approach would however risk itself producing greater memory demands that can be provided by the executing system; for empirical data it might be that the set of unique design matrices is very large, and therefore it is storage of these data that becomes prohibitive. Maybe it could pre-compute data for the most prevalent cases only, and perform computations on-the-fly for more rare cases? An alternative solution to this computational demand might be to utilise a drastically reduced number of unique shuffles, parameterising the tail of the null distribution to estimate the location of the *p*=0.05 threshold, as exemplified in ([Winkler et al., 2016](https://www.sciencedirect.com/science/article/pii/S1053811916301902)). I'd like to implement this at some point ([Pull Request #1799](https://github.com/MRtrix3/mrtrix3/issues/1799)); but as has increasingly become the case, I simply don't have enough time in the day to implement features that do not yield measures that contribute to career progression.

Nevertheless, while this may be fairly impractical for a dataset of the size of that investigated by the authors, it does show how interrogation of the underlying implementation may have exposed the presence of an alternative code branch that did not exhibit the manifest memory usage problem, which in turn may have assisted in isolating the origin of that issue.

## Personal impact

Given that I am trying to do this post mortem with full honesty and transparency, I think I am obliged to say that the amount of frustration that this particular situation has caused for me personally is non-zero. That is not however to say that I hold any animosity toward the authors of the ModelArray manuscript, contributors to that software package, or any researchers whom have found utility within it. There are a multitude of factors that all conspired to make the outcome of this process sub-optimal:

1.  The C++ programming language is relatively opaque to almost all scientific researchers. This makes it exceptionally rare for anyone external to the core development team to make contributions within our ecosystem. It is therefore more likely for there to be explicit investment that are in direct competition to our software project rather than fixing or extending it, even if the volume of effort required for the latter could conceivably have been smaller.
    
2.  This article was submitted for review at a time during which my existing multiplicity of obligations was further exacerbated by taking on a part-time industry fellowship. It was inevitable that there would be causalities during this time. The first sacrifice was the ability to provide personalised assistance to some 2,000 individuals none of whom pay my salary. That is an intentionally blunt way to put it, but I'm trying to highlight the impossibility of the situation I was (and still somewhat am) in; I hope to write something more extensive in the future on the demands of research software maintenance and its incompatibility with the existing scholarship model. Unfortunately this resulted in the observations made by the authors not immediately receiving the level of attention from my end that it deserved.

3.  With losses to the core *MRtrix3* development team over time, and an inability to recruit new core team members or obtain the requisite funding to employ a team of software engineers dedicated to the project, I have inherited responsibility for an exceptionally large breadth of code, which this and myriad other scenarios have exposed as untenable.

4.  I still am yet to receive literature credit for the broad range of technical enhancements made to the Fixel-Based Analysis framework since the departure of original developer @dave that have required *substantial* time investment. Time spent resolving issues identified by the community incurs an opportunity cost, further delaying the progress or publication of my own work, which is now damaging my career sustainability prospects. That cost grows with the magnitude of whatever it is that requires redress or rectification. This is on the extreme end of that spectrum, being an manuscript predicated on a major deficiency in your implementation, which inevitably is going to be experienced as a large weight on that pile, regardless of intent of authors.
    
5.  The fact that an oversight constituting perhaps only *tens* of lines of code, among a changeset consisting of some ten *thousand* lines of code, can elicit a public critique and considerable investment in creation of a direct competitor, exemplifies how the expectations placed upon researchers who write software---regardless of whether designated explicitly as research software engineers---are immense in not only *quantity* but also in *quality*. I've already been through [one experience](https://www.sciencedirect.com/science/article/pii/S105381192200859X) of a tiny software change resulting in erroneous scientific outcomes for another individual, and for there to be more in the future is likely an inevitability. This *burden of expectation* is I think something that warrants recognition in the wider research community; I hope to pontificate more on this in the future.

6.  I have [explicitly proclaimed in the public domain](https://www.sciencedirect.com/science/article/pii/S105381192200859X) that proximal and public communication between researchers and the developers of research software is critical for the robustness and quality of the corpus of scientific research. This story is one of unfortunately many where I have been hypocritical in this respect.

7.  Just in case that all wasn't enough: for those not aware I have a chronic health condition that can limit the number of work hours I can achieve. I include this here not to elicit sympathy, but in the hope that the authors will be forgiving of my long turnaround, and also so that others whom have been let down by my lack of support of late can understand that it is due not to indifference or selfishness, but incapacity.

## Conclusion

I do not want for anyone to infer from the above that I consider the authors / creators of ModelArray to have misstepped in any way. They identified a deficiency in the current capabilities within the domain, implemented a solution to such, and provided it openly to the research community. Any negative consequences of such at my end are my responsibility alone.

I want to tie this all back to my peer review of this article. Its core feature was vaguely as follows:
*The excessive memory usage in `fixelcfestats` was likely to be an outright bug or oversight on my part; and that therefore predicating the impact or novelty of their publication on claims of reduced memory consumption compared to the established alternative would be completely undermined if it were to turn out that said memory usage could be reasonably trivially rectified.*
I instead encouraged that the authors focus on the novel scientific capabilities of their software compared to `fixelcfestats`: in particular not being constrained by the limitation of the General Linear Model. This transition is I think visible in the evolution of their work from the [preprint](https://www.biorxiv.org/content/10.1101/2022.07.12.499631v1.full) to the [published article](https://www.sciencedirect.com/science/article/pii/S1053811923001830). I hope that the authors agree given the evidence presented above that this was the right decision. I fully endorse the presentation of fixel-based statistical analysis using more complex statistical models as a novel contribution to the domain.

Another justification for wanting to explain this story in full is that I have experienced multiple interactions where researchers seemingly consider open source software to be *immutable*, and as a consequence end up tying themselves around in knots trying to either apply some sort of high-level wrapping around that software, or re-implement components from scratch just to gain requisite access to the internal operation. I encourage people to always consider the prospect that, to achieve their target outcome, modification of existing software may in fact be more expedient than avoiding doing so.

Given it is quite likely that this `fixelcfestats` memory consumption may be causing barriers for a greater number of researchers, I'm going to do my best to finalise those changes and get them integrated into a tagged release. For anyone competent with `git` and compiling from source, the source code [is publicly available](https://github.com/MRtrix3/mrtrix3/pull/2269), so anyone can use it already. Having finally had the opportunity to revisit this issue, I do however think that I still need to invest more effort; having all FBAs incur a 40% performance penalty just to support rare use cases would I think not be well-received.

-----

That's all from me for now.

Congratulations to anyone successful in getting all of the way through that.

Hoping to be in greater communication in the future.

Best regards
Rob

---

*[View comments on the community site](https://community.mrtrix.org/t/8503)*

            