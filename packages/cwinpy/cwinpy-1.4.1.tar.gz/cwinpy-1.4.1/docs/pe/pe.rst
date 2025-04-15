#################################
Known pulsar parameter estimation
#################################

CWInPy can be used for perform Bayesian inference on gravitational-wave data to estimate the
gravitational-wave signal parameters for emission from a known pulsar. To sample from the joint
parameter posterior distributions, CWInPy uses the `bilby
<https://lscsoft.docs.ligo.org/bilby/>`_ package as an interface to a variety of stochastic sampling
methods.

CWInPy comes with an executable, ``cwinpy_pe``, for performing this analysis, which tries to
emulate, as much as possible, the functionality from the `LALSuite
<https://lscsoft.docs.ligo.org/lalsuite/>`_ code ``lalpulsar_parameter_estimation_nested`` (formerly
``lalapps_pulsar_parameter_estimation_nested``) described in [1]_.

There is also an API for running this analysis from within a Python shell or script as described
:ref:`below<Parameter estimation API>`.

Running the analysis
--------------------

The ``cwinpy_pe`` executable, and :ref:`API<Parameter estimation API>`, can be used to perform
parameter estimation over a variety of signal parameter both on real data or simulated data. We will
cover some examples of both cases and show equivalent ways of running the analysis via the use of:
command line arguments to the ``cwinpy_pe`` executable, a configuration file, or the
:ref:`API<Parameter estimation API>`. The current command line arguments for ``cwinpy_pe`` are given
:ref:`below<pe Command line arguments>`.

Example: single detector data
=============================

In the first example we will show how to perform parameter estimation on some real
gravitational-wave data. We will use a short segment of data from the O1 run of the LIGO detectors
(the whole of which can be found on the `GWOSC website
<https://gwosc.org/archive/O1/>`_) between GPS times of 1132444817 and 1136419217. The
O1 dataset contains a set of simulated pulsar signals that have been `"injected"
<https://gwosc.org/o1_inj/>`_ into it. We will look at the injected signal named
``PULSAR8``, the parameters of which can be found at `this link
<https://gwosc.org/static/injections/o1/cw_injections.html>`_.

The data we will use in this example is from the `LIGO Hanford <https://www.ligo.caltech.edu/WA>`_
detector (abbreviated to "H1") and has been heterodyned using the known phase evolution of the
simulated signal (see the description :ref:`here<Heterodyned Data>`), and low-pass filtered and
down-sampled to a rate of one sample per minute. This data file (in a gzipped format) can be
downloaded here: :download:`fine-H1-PULSAR08.txt.gz <data/fine-H1-PULSAR08.txt.gz>`.

A Tempo(2)-style [2]_ pulsar parameter (``.par``) file for this simulated signal is reproduced below
and can be downloaded :download:`here <data/PULSAR08.par>`, where it should be noted that the ``F0``
and ``F1`` parameters in that file are the expected **rotation** frequency and frequency derivative
of the putative pulsar, so they are **half** those of the simulated gravitational-wave signal in the
data.

.. literalinclude:: data/PULSAR08.par
   :language: text

Here we will try and estimate four of the signal's parameters: the gravitational-wave amplitude
:math:`h_0`; the inclination angle :math:`\iota` of the rotation axis to the line-of-sight; the
initial rotational phase of the signal :math:`\phi_0`; and the polarisation angle of the source
:math:`\psi`. To do this we have to define a file containing the prior probability distributions for
these parameters. We can define the priors in a file as described in the documentation for the
`bilby package <https://lscsoft.docs.ligo.org/bilby/prior.html>`_, which is reproduced below and can
be downloaded :download:`here <data/example1_prior.txt>`:

.. literalinclude:: data/example1_prior.txt
   :language: python

Here we have set the prior on :math:`h_0` to be uniform between 0 and 10\ :sup:`-22`, where in this
case the maximum has been chosen to be large compared to the expected signal strength. The
combination of the :math:`\iota` and :math:`\psi` parameters has been chosen to be uniform over a
sphere, which means using a uniform prior over :math:`\psi` between 0 and :math:`\pi/2` (there is a
degeneracy meaning this doesn't have to cover the full range between 0 and :math:`2\pi` [1]_ [3]_),
and a sine distribution prior on :math:`\iota` (equivalently one could use a uniform prior on a
:math:`\cos{\iota}` parameter between -1 and 1). The :math:`\phi_0` parameter is the initial
rotational phase at a given epoch, so only needs to span 0 to :math:`\pi` to cover the full phase of
the equivalent gravitational-wave phase parameter in the case where the source is emitting at twice
the rotational frequency.

With the data at hand, and the priors defined, the analysis can now be run. It is recommended to run
by setting up a configuration file, although as mentioned equivalent command line arguments can be
passed to ``cwinpy_pe`` (or a combination of a configuration file and command line arguments may
be useful if defining some fixed setting for many analyses in the file, but making minor changes for
individual cases on the command line). A configuration file for this example is shown below, with
comments describing the parameters given inline:

.. literalinclude:: data/example1_config.ini
   :language: ini

.. note::

   When using the `dynesty <https://dynesty.readthedocs.io/en/latest/>`_ sampler (as wrapped through
   `bilby <https://lscsoft.docs.ligo.org/bilby/>`_) it will default to use the ``rwalk`` sampling
   method. This has been found to work well and be the quickest option for normal running. A
   discussion of the bilby-specific different dynesty sampling options can be found
   `here <https://lscsoft.docs.ligo.org/bilby/dynesty-guide.html#bilby-specific-implementation-details>`__,
   while discussion of the options in dynesty itself can be found
   `here <https://dynesty.readthedocs.io/en/latest/quickstart.html#sampling-options>`__.

The analysis can then be run using:

.. code-block:: bash

   cwinpy_pe --config example1_config.ini

which should only take a few minutes, with information on the run output to the terminal.

This will create a directory called ``example1`` containing: the results as a bilby ``Results``
object saved, by default, in an `HDF5
<https://en.wikipedia.org/wiki/Hierarchical_Data_Format#HDF5>`_
format file called ``example1_result.hdf5`` (see `here
<https://lscsoft.docs.ligo.org/bilby/bilby-output.html#the-result-file>`__ for information on reading
this information within Python); and (due to the setting of ``'plot': True`` in the
``sampler_kwargs`` dictionary), a "`corner <https://corner.readthedocs.io/en/latest/>`_ plot" in the
file ``example1_corner.png`` showing 1D and 2D marginalised posterior probability distributions for
each parameter, and pair of parameters. To instead save the results to a  `JSON
<https://www.json.org/>`_ format file you would include ``"save": "json"`` in the ``sampler_kwargs``
dictionary. To gzip the JSON file you would include ``"gzip": True`` in the ``sampler_kwargs``
dictionary.

.. thumbnail:: data/example1/example1_corner.png
   :width: 300px
   :align: center

.. note::

   The slight offset seen in the recovered phase is related to the uncompensated 150 microsec time
   delay in the actuation function used to generate the simulated signal as discussed in [4]_.

The code should also output the natural logarithm of the signal model `evidence
<https://en.wikipedia.org/wiki/Marginal_likelihood>`_ (``log_evidence``), noise-only model evidence
(``log_noise_evidence``), and `Bayes factor <https://en.wikipedia.org/wiki/Bayes_factor>`_ between
those two models, and estimates of the uncertainties on the signal model evidence.

.. code-block:: none

   log_noise_evidence: 869768.909
   log_evidence: 870014.455 ± 0.180
   log_bayes_factor: 245.547 ± 0.180

If running the example you should find an identical noise evidence value, although the signal model
evidence, and therefore Bayes factor, and its uncertainty may vary slightly due to the stochastic
nature of the sampling process. These values can also be extracted from the results file called
``example1_result.hdf5``.

Rather than using the configuration file, all the arguments could be given on the command line
(although using the configuration file is *highly* recommended), with the following command:

.. code-block:: bash

   cwinpy_pe --detector H1 --par-file PULSAR08.par --data-file fine-H1-PULSAR08.txt.gz --outdir example1 --label example1 --sampler dynesty --sampler-kwargs "{'Nlive':1000,'sample':'rwalk','plot':True}" --prior example1_prior.txt --show-truths

where it should be noted that the ``--sampler-kwargs`` dictionary argument must be given within
quotation marks.

Example: multi-detector data
=============================

In this example we will replicate the analysis from the first `example
<#example-single-detector-data>`_, but will use O1 data from more than one detector. It will again
look at the hardware injection signal named `PULSAR8
<https://gwosc.org/static/injections/o1/cw_injections.html>`_ and use the same
parameter file as given above.

The data we will use in this example is a short segment (between GPS times of 1132444817 and
1136398891) from both the `LIGO Hanford <https://www.ligo.caltech.edu/WA>`_ detector (abbreviated to
"H1") and the `LIGO Livingston <https://www.ligo.caltech.edu/LA>`_ detector (abbreviated to "L1").
Both sets of data have been heterodyned using the known phase evolution of the simulated signal (see
the description :ref:`here<Heterodyned Data>`), and low-pass filtered and down-sampled to a rate of
one sample per minute. The data files (in a gzipped format) can be downloaded here:
:download:`fine-H1-PULSAR08.txt.gz <data/fine-H1-PULSAR08.txt.gz>` and
:download:`fine-L1-PULSAR08.txt.gz <data/fine-L1-PULSAR08.txt.gz>`. We will use an identical prior
file to that in the first example, but rename it :download:`example2_prior.txt
<data/example2_prior.txt>`.

The configuration file for this example is shown below, with comments describing the parameter given
inline:

.. literalinclude:: data/example2_config.ini
   :language: ini

The analysis can then be run using:

.. code-block:: bash

   cwinpy_pe --config example2_config.ini

This will create a directory called ``example2`` containing: the results as a bilby ``Results``
object saved, by default, in an `HDF5
<https://en.wikipedia.org/wiki/Hierarchical_Data_Format#HDF5>`_ format file called
``example2_result.hdf5`` (see `here
<https://lscsoft.docs.ligo.org/bilby/bilby-output.html#the-result-file>`__ for information on reading
this information within Python); and (due to the setting of ``'plot': True`` in the
``sampler_kwargs`` dictionary), a "`corner <https://corner.readthedocs.io/en/latest/>`_ plot" in the
file ``example2_corner.png`` showing 1D and 2D marginalised posterior probability distributions for
each parameter, and pair of parameters.

.. thumbnail:: data/example2/example2_corner.png
   :width: 300px
   :align: center

.. note::

   The slight offset seen in the recovered phase is related to the uncompensated 150 microsec time
   delay in the actuation function used to generate the simulated signal as discuss in [4]_.

The natural logarithms of the signal model `evidence
<https://en.wikipedia.org/wiki/Marginal_likelihood>`_ (``log_evidence``), noise-only model evidence
(``log_noise_evidence``) and `Bayes factor
<https://en.wikipedia.org/wiki/Bayes_factor>`_ (``log_bayes_factor``) output for this example are 

.. code-block:: none

   log_noise_evidence: 1492439.107
   log_evidence: 1492888.344 ± 0.186
   log_bayes_factor: 449.237 ± 0.186

If running the example you should find an identical noise evidence value, although the signal model
evidence, and therefore Bayes factor, and its uncertainty may vary slightly due to the stochastic
nature of the sampling process. These values can also be extracted from the results file called
``example2_result.hdf5``.

The equivalent full command line arguments that could be used are:

.. code-block:: bash

   cwinpy_pe --detector H1 --detector L1 --par-file PULSAR08.par --data-file fine-H1-PULSAR08.txt.gz --data-file fine-L1-PULSAR08.txt.gz --outdir example2 --label example2 --sampler dynesty --sampler-kwargs "{'Nlive':1000,'sample':'rwalk','plot':True}" --prior example2_prior.txt --show-truths

Example: a simulated transient-continuous signal
================================================

It is interesting to consider signals that do not have a constant amplitude, but are transitory on
time scales of days-to-weeks-months (e.g., [8]_, [9]_, [10]_); so-called "*transient-continuous*" signals.
These might occur following a pulsar glitch [11]_. CWInPy is able to simulate and infer the
parameters of two classes of these signals, which use the normal continuous signal model modulated
by a particular window function:

1. a rectangular window where the signal abruptly turns on then off;
2. an exponentially decaying window, where there is an abrupt start followed by an exponential decay.

Both models are defined by a start time, e.g., the time of an observed pulsar glitch, and a
timescale :math:`\tau`, which defines the duration of the rectangular window model and the decay
time constant for the exponential window model.

In this example, we will simulate a transient signal with a rectangular window in data from the both
the `LIGO Hanford <https://www.ligo.caltech.edu/WA>`_ detector (abbreviated to "H1") and the `LIGO
Livingston <https://www.ligo.caltech.edu/LA>`_ detector between 01:46:25 on 14th Sept 2011 (a GPS
time of 1000000000) and 01:46:25 on 18th Sept 2011.

To simulate a transient signal, the Tempo(2)-style pulsar parameter (``.par``) file needs to
contain the following parameters:

* ``TRANSIENTWINDOWTYPE``: this can be ``RECT`` (rectangular window) or ``EXP`` (exponential
  window);
* ``TRANSIENTSTARTTIME``: the time at which the signal "turns-on". This should be give as in
  Modified Julian Day (MJD) format, which is how glitch times are defined in Tempo(2);
* ``TRANSIENTTAU``: the signal duration (rectangular window) or decay time constant (exponential
  window) in days.

For this example, the ``.par`` file we used defined a model with a rectangular window. It and can
be downloaded :download:`here <data/TRANSIENT.par>` and is reproduced below.

.. literalinclude:: data/TRANSIENT.par
   :language: text

To estimate the parameters of the transient signal model they must be included in the file defining
the required prior probability distributions. The prior file we use is reproduced below and can be
downloaded :download:`here <data/example3_prior.txt>`:

.. literalinclude:: data/example3_prior.txt
   :language: python

If setting the ``TRANSIENTSTARTTIME`` and ``TRANSIENTTAU`` to use MJD and days, respectively, in the
prior file (to be consistent with the ``.par`` file) then the ``unit`` key for each prior must be
set to ``d`` (for day). Otherwise the values will be expected in GPS seconds and seconds. In this
case, a Gaussian prior is used for the start time with a mean given by the actual simulated start
time and a standard deviation of 0.5 days, and a uniform prior is used for the duration within a
range from 0.1 to 3 days. 

.. note::

   You can use the :class:`astropy.time.Time` class to convert between GPS and MJD, e.g.:

   >>> from astropy.time import Time
   >>> mjd = Time(1234567890, format="gps", scale="tdb").mjd

   or vice versa:

   >>> gps = Time(1234567890, format="mjd", scale="tdb").gps

A configuration file that can be passed to ``cwinpy_pe`` for this example is shown below, with
comments describing the parameters given inline:

.. literalinclude:: data/example3_config.ini
   :language: ini

This can then be run with:

.. code-block:: bash

   cwinpy_pe --config example3_config.ini

which produces the following posteriors:

.. thumbnail:: data/example3/example3_corner.png
   :width: 300px
   :align: center

and the following signal model and noise model log evidence values:

.. code-block:: none

   ln_noise_evidence: 1274081.150
   ln_evidence: 1274102.482 +/-  0.189
   ln_bayes_factor: 21.331 +/-  0.189

Running on multiple sources
---------------------------

You may have multiple real sources for which you want to perform parameter estimation, or you may
want to simulate data from many sources. If you have a multicore machine or access to a computer
cluster with `HTCondor <https://htcondor.readthedocs.io>`__ installed you can use CWInPy to
create a set of analysis jobs, in the form of an HTCondor `DAG
<https://htcondor.readthedocs.io/en/v8_8_4/users-manual/dagman-applications.html>`_, for each
source. This makes use of `PyCondor <https://jrbourbeau.github.io/pycondor/installation.html>`_,
which is installed as one of the requirements for CWInPy.

To set up a DAG to analyse real data for multiple pulsars you need to have certain datasets and
files organised in a particular way. You must have a set of Tempo(2)-style pulsar parameter files,
with only one for each pulsar you wish to analyse, which each contain a ``PSRJ`` value giving the
pulsar's name, e.g.,

.. code-block:: bash

   PSRJ  J0534+2200

You also need to have a directory structure where the heterodyned data (see :ref:`here<Heterodyned
Data>`) from individual detectors are in distinct directories (if you want specify each file for
each pulsar individually in a dictionary this can be done instead, but requires more manual
editing). Also, if there is data from both the a potential signal at the sources rotation frequency
*and* twice the rotation frequency, then these should also be in distinct directories. The
heterodyned data file for a particular pulsar must contain the ``PSRJ`` name of the pulsar, as given
in the associated parameter file, either in the file name or the file directory path.

An example of such a directory tree structure might be:

.. code-block:: bash

   root
    ├── pulsars              # directory containing pulsar parameter files
    ├── priors               # directory containing pulsar prior distribution files
    ├── detector1            # directory containing data for first detector
    |    ├── 1f              # directory containing data from first detector at the source rotation frequency
    |    |    ├── pulsar1    # directory containing data from first detector, at the rotation frequency for first pulsar (could be named using the pulsar's PSRJ name)
    |    |    ├── pulsar2    # directory containing data from first detector, at the rotation frequency for second pulsar (could be named using the pulsar's PSRJ name)
    |    |    └── ...
    |    └── 2f
    |         ├── pulsar1    # directory containing data from first detector, at twice the rotation frequency for first pulsar (could be named using the pulsar's PSRJ name)
    |         ├── pulsar2    # directory containing data from first detector, at twice the rotation frequency for second pulsar (could be named using the pulsar's PSRJ name)
    |         └── ...
    ├── detector2            # directory contain data for second detector
    |    └── ...
    └── ...

The DAG for the analysis can be created using the ``cwinpy_pe_pipeline`` executable, which requires
a configuration file as its only input. An example configuration file, based on the above directory
tree structure is given below. Comments about each input parameter, and different potential input
options are given inline; some input parameters are also commented out using a ``;`` if the default
values are appropriate. For more information on the various HTCondor options see the `user manual
<https://htcondor.readthedocs.io/en/v8_8_4/users-manual/index.html>`_.

.. literalinclude:: cwinpy_pe_pipeline.ini

Once the configuration file is created (called, say, ``cwinpy_pe_pipeline.ini``), the Condor DAG dag
can be generated with:

.. code-block:: bash

    cwinpy_pe_pipeline cwinpy_pe_pipeline.ini

This will, using the defaults and values in the above file, generate the following directory tree
structure:

.. code-block:: bash

   root
    ├── results            # directory to contain the results for all pulsars
    |    ├── pulsar1       # directory to contain the results for pulsar1 (named using the PSRJ name)
    |    ├── pulsar1       # directory to contain the results for pulsar2 (named using the PSRJ name)
    |    └── ...
    ├── configs            # directory containing the cwinpy_pe configuration files for each pulsar
    |    ├── pulsar1.ini   # cwinpy_pe configuration file for pulsar1 (named using the PSRJ name)
    |    ├── pulsar2.ini   # cwinpy_pe configuration file for pulsar2 (named using the PSRJ name)
    |    └── ...
    ├── submit             # directory containing the DAG and job submit files
    |    ├── dag_cwinpy_pe.submit      # Condor DAG submit file
    |    ├── cwinpy_pe_H1L1_pulsar1.submit  # cwinpy_pe job submit file for pulsar1
    |    ├── cwinpy_pe_H1L1_pulsar2.submit  # cwinpy_pe job submit file for pulsar2
    |    └── ...
    └── log                # directory for the job log files

By default, if passed data for multiple detectors, the parameter estimation will be performed with
a likelihood that coherently combines the data from all detectors. To also include parameter
estimation using data from each detector individually, the ``[pe]`` section of the configuration
file should contain

.. code-block:: bash

   incoherent = True

The submit files and the final output parameter estimation files will show the combination of
detectors used in the filename.

If the original ``cwinpy_pe_pipeline`` configuration file contained the line:

.. code-block:: bash

   submitdag = True

in the ``[dag]`` section, then the DAG will automatically have been submitted, otherwise it could be
submitted with:

.. code-block:: bash

   condor_submit_dag /root/submit/dag_cwinpy_pe.submit

.. note::

   If running on LIGO Scientific Collaboration computing clusters the ``acounting_group`` value must
   be specified and be a valid tag. Valid tag names can be found `here
   <https://accounting.ligo.org/user>`__ unless custom values for a specific cluster are allowed.

.. _pe Command line arguments:

Command line arguments
----------------------

The command line arguments for ``cwinpy_pe`` can be found using:

.. command-output:: cwinpy_pe --help

Parameter estimation API
------------------------

.. automodule:: cwinpy.pe.pe
   :members: pe, pe_pipeline

.. automodule:: cwinpy.pe.testing
   :members: PEPPPlotsDAG, generate_pp_plots

Parameter estimation utilities API
----------------------------------

.. automodule:: cwinpy.pe.peutils
   :members:

``cwinpy_pe`` references
------------------------

.. [1] M. Pitkin, M. Isi, J. Veitch & G. Woan, `arXiv:1705.08978v1
       <https://arxiv.org/abs/1705.08978v1>`_, 2017.
.. [2] `G. B. Hobbs, R. T. Edwards & R. N. Manchester
   <https://ui.adsabs.harvard.edu/?#abs/2006MNRAS.369..655H>`_,
   *MNRAS*, **369**, 655-672 (2006)
.. [3] `D. I. Jones <https://ui.adsabs.harvard.edu/abs/2015MNRAS.453...53J>`_,
   *MNRAS*, **453**, 53-66 (2015)
.. [4] `C. Biwer et al. <https://ui.adsabs.harvard.edu/abs/2017PhRvD..95f2002B/abstract>`_,
   *PRD*, **95**, 062002 (2017)
.. [5] L. Barsotti, S. Gras, M. Evans, P. Fritschel,
   `LIGO T1800044-v5 <https://dcc.ligo.org/LIGO-T1800044/public>`_ (2018)
.. [6] `T. Sidery et al. <https://arxiv.org/abs/1312.6013>`_,
   *PRD*, **89**, 084060 (2014)
.. [7] `B. P. Abbott et al. <https://ui.adsabs.harvard.edu/abs/2019ApJ...879...10A/abstract>`_,
   *ApJ*, **879**, p. 28 (2019)
.. [8] `R. Prix, S. Giampanis, S. & C. Messenger, C. <https://ui.adsabs.harvard.edu/abs/2011PhRvD..84b3007P/abstract>`_,
   *PRD*, **84**, 023007 (2011)
.. [9] `D. Keitel et al. <https://ui.adsabs.harvard.edu/abs/2019PhRvD.100f4058K/abstract>`_,
   *PRD*, **100**, 064058 (2019)
.. [10] R. Abbott et al., `arXiv:2112.10990 <https://arxiv.org/abs/2112.10990>`_, 2021.
.. [11] `G. Yim & D. I. Jones <https://ui.adsabs.harvard.edu/abs/2020MNRAS.498.3138Y/abstract>`_,
   *MNRAS*, **498**, 3138-3152 (2020)