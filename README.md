<h3>
<a name="user-content-authors" class="anchor" href="#dependencies" aria-hidden="true"><span class="octicon octicon-link"></span></a>Automated Malware Analysis</h3>

Automated malware analysis systems added memory analysis capabilities as part of their arsenal. These systems execute a sample inside a controlled environment for a configurable amount of time. When time is up, they grab a memory dump and run a set of memory analysis utilities/plugins in search for malicious artifacts. While this process yield great results and is a great technique to dissect malware, it comes with some disadvantages:

Taking memory dumps requires accurate timing - If we take it at the wrong time, we may “miss the action” - malicious artifacts may not exist yet or already disappear from memory.
Also, Artifacts taken from a single memory dump lack context since there is no baseline memory dump to compare
it with. This means it is difficult to make meaningful conclusions without information about when the artifact was created,
modified, deleted, etc.

This project aims to solve these disadvantages by introducing Trigger-Based analysis - Taking multiple memory dumps during execution in "strategic moments" by analyzing API calls, CPU performance counters, and tracing execution with Dynamic Binary Instrumentation techniques. Once done executing, our system performs differential analysis on the resulting memory dumps.

This project was built on top of Cuckoo Sandbox, however, the techniques are generic may be trivially applied to other analysis machines. 

For more information: Read the White Paper and view the Slides (WP_AND_PRESENTATION directory)

Black Hat Arsenal 2014: 
https://www.blackhat.com/us-14/arsenal.html#Teller



<h3>
<a name="user-content-authors" class="anchor" href="#dependencies" aria-hidden="true"><span class="octicon octicon-link"></span></a>Dependencies</h3>
<ul class="task-list">
<li>Cuckoo Sandbox dependencies.</li>
<li>In order to use the heap entropy calculator plugin, copy heap_entropy.py from Volatility directory (under master directory) to the Volatility plugins directory.</li>
<li>In order to use the monitorCPU trigger, you will have to run CPU.exe on your analysis machine (and grab a snapshot)</li>
<li>In order to support precise trigger-based analysis (suspending/resuming VM, grabbing memory dumps, etc.) we modified cuckoomon.dll. 
Note! The dll that is provided in this fork is the modified version.</li>
<li>We recommend using QEMU as the VM platform in order to leverage Virtual Machine Introspection. In order to do so, you should install the following software: Qemu 1.7.0, libvirt 1.0 and libvmi.
To enable live introspection and memory dump patching with Volatility, you will have to add the qemu address space plugin (if you are using Volatility 2.4, it comes with the default installation). The plugin can be found under our Volatility directory and should be placed in volatility/plugins/addrspaces/qemuelf.py. 
Note! Parsing Qemuelf dump is currently not supported by Volatility. In order to fix the problem, you can pass a --dtb flag to vol.py with any plugin. If you want to add it automatically, you will have to add a dtb variable in the Qemuelf class.</li>
</ul>

<h3>
<a name="user-content-authors" class="anchor" href="#dependencies" aria-hidden="true"><span class="octicon octicon-link"></span></a>Usage</h3>
<ul class="task-list">
<li>Download ZIP and extract</li>
<li>Configure Cuckoo (http://docs.cuckoosandbox.org/en/0.4.2/installation/)</li>
<li>Run Cuckoo.py</li>
</ul>

<h3>
<a name="user-content-authors" class="anchor" href="#dependencies" aria-hidden="true"><span class="octicon octicon-link"></span></a>Configuring Cuckoo to run automated memory analysis</h3>
<ul class="task-list">
<li>In processing.conf, enable memory analysis:
<pre><code>[memoryanalysis]
enabled = yes
</code></pre>
</li>
<li>Configure the memory analysis environment to your needs.
You will find a new file, memoryanalysis.conf, in which you can set all the parameters for your analysis. This file includes a basic block section:
<pre><code>[basic]
trigger_based = on
time_based = off
</code></pre>
This block configures Time (interval)-Based/Trigger-Based analysis. Please make sure you enable at least one of them.
In the time-based section, you can configure the number of seconds to sleep between taking memory dumps:
<pre><code>[time_based]
time_to_sleep_before_dump_in_seconds = 30
</code></pre>
In the memory diff plugins section, you can choose to enable or disable the analysis plugins.
In case they are enabled, they will appear under every memory dump in the generated JSON report and will highlight which artifacts were added, modified or deleted.
<pre><code>[diff_hidden_processes]
enabled = yes
desc = Detects new hidden processes
</code></pre>
Under the trigger points section, you can configure each trigger:
<pre><code>[Trigger_VirtualProtectEx]
# Enable / Disable
enabled = yes
# Whether to dump memory on this trigger
dump_memory = yes
# Whether to pause execution to enable live VMI inspection
break_on_volshell = no
# Which plugins to run when this trigger happens
run_plugins = diff_processes
# Whether to run automatic plugins on the trigger, based on its type.
run_smart_plugins = yes
# Whether to pause execution and open a python shell. 
# This gives the user the power to set more breakpoints on-demand.
breakpoint = off
# Max number of times for this trigger.
times = 1
</code></pre>
</li>
<li>If you want to use the regular Volatility plugins without doing any diff logic, just configure it in memory.conf, and the results will appear under every memory dump (the new report format is described in the following section).
Note: We wrapped existing Volatility plugins which were not wrapped by Cuckoo, they can also be used.</li>

</ul>
<h3>
<a name="user-content-authors" class="anchor" href="#dependencies" aria-hidden="true"><span class="octicon octicon-link"></span></a>Changes in the report</h3>
Cuckoo generates a JSON report (the data in it is used to generate the HTML report that can be viewed with the Cuckoo web server).
We made a few changes in this JSON report to include the memory analysis results, too.

report.json without Trigger-Based Memory Analysis:
<pre><code>
{
	'memory' : {
			'malfind' : {} ...
		   }
}
</code></pre>
report.json with Trigger-Based Memory Analysis (A key is created for each memory dump):
<pre><code>
{
	'dumps' : {
		'Dump_1' : {
				'path' : '...'
				'meta' : {
						'trigger' : {...},
						'time' : "..."
					 }
		
			   } ,
		'Dump_2' : {...}
	}
}
</code></pre>

<h3>
<a name="user-content-authors" class="anchor" href="#dependencies" aria-hidden="true"><span class="octicon octicon-link"></span></a>New Plugins</h3>
We added new differential analysis plugins which you can enable:
<ul class="task-list">
<li>Heap entropy: Calculates the current heap entropy of a process.</li>
<li>AVStrings: Finds Anti-Virus strings in the dump.</li>
<li>Modified PE Header: Finds incomplete PE headers.</li>
</ul>

<h3>
<a name="user-content-authors" class="anchor" href="#dependencies" aria-hidden="true"><span class="octicon octicon-link"></span></a>Changes Log</h3>
Changes were made in Cuckoo's core and different modules to enable triggering memory dumps. Before every change, a comment "CHANGED: [..]" was added.
