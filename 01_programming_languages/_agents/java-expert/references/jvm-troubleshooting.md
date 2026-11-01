# JVM Troubleshooting Handbook: diagnostic reference (PermGen era, examples on HotSpot 1.5 to 1.7)

Source: "JVM Troubleshooting Guide/Handbook" (P.-H. Charbonneau and I. Tsagklis, Java Code Geeks). Citations in the format (JVM p.N) point to the PDF page.

## Contents

0. Era notice
1. Conventions
2. Mental model of the JVM according to the text
3. Diagnostic procedures (symptom, cause, investigation, fix)
4. Flags and tools cited, with the text's version
5. Case studies: what each one illustrates
6. Version assumptions of the text and gaps

---

## 0. Era notice

The handbook describes the Oracle HotSpot JVM of the PermGen era. Versions appear in the examples, not in a general scope statement: HotSpot 1.5 (JVM p.27), 1.6 (JVM p.42, 59, 60) and 1.7 (JVM p.23, 33, 79); the text explicitly ties PermGen to JDK 1.7 (JVM p.23) and to the era before Java 8 (JVM p.21). The cases are on Java EE servers (WebLogic, JBoss, WebSphere, OSB) over Solaris, AIX and Windows, with a strong presence of 32-bit JVMs. The few passages about Java 8 come from a beta build and were already forward-looking when written (JVM p.21–26).

Rules of use for the agent:

- Treat every claim in this file as "what the text says for that era", not as the current state of the platform.
- The release notes provided (JDK 11 to 26) do not cover garbage collectors, PermGen or diagnostic tools. There is therefore no source in the package to confirm or correct the handbook's flags, error messages, tools or defaults. When the question depends on that, say that the text does not cover what changed afterwards and that the documentation of the JVM in use must be checked.
- The author's numbers are rules of thumb of the time, not official values: heap of up to 2 GB on 32-bit and 3 to 4 GB on 64-bit (JVM p.11); about 50% occupancy after a major collection, given in the example of a 64-bit VM with a 3 GB heap (JVM p.12); reduction of about 256 MB of heap on 32-bit (JVM p.89). The author himself says every environment is unique (JVM p.8).

## 1. Conventions

- DATED: concept or flag tied to the era of the text. DEPENDS ON VERSION: behavior the text attributes to a specific version. [inference]: my own link, not stated by the book.
- Quotation marks only for names, flags, log excerpts and short English quotes; the rest is paraphrase.
- When the text lacks one of the four elements (symptom, cause, investigation, fix), this is stated.

---

## 2. Mental model of the JVM according to the text

### 2.1 Three memory spaces in HotSpot

The HotSpot process is described as three areas competing with each other (JVM p.3, p.9):

- **Java Heap**: holds object instances. Maximum and minimum via `-Xmx` and `-Xms` (example 1024m). Monitored by verbose GC, JMX, JConsole and similar (JVM p.3). Divided into young generation (YoungGen, nursery) and old generation (OldGen, tenured) in all vendors (JVM p.9).
- **PermGen (permanent generation)**: HotSpot-specific. Holds Class objects (names and methods), internal JVM objects and JIT optimization data. Sized by `-XX:MaxPermSize` and `-XX:PermSize` (examples 512m and 256m) (JVM p.3–4). The text considers it fairly static, except with third-party tools or Reflection that depend on dynamic class loading (JVM p.5). DATED.
- **Native Heap (C-Heap)**: not directly configurable. Contains mapped files (MMAP), native code of the JVM and third parties and, as seen later, thread stacks (JVM p.4, p.90). Capacity on 32-bit: 4 GB minus heap minus PermGen. On 64-bit: physical RAM plus virtual memory, minus heap, PermGen and the process size (JVM p.4). Monitoring: process size (Windows and Linux), `pmap` (Solaris and Linux), `svmon` (AIX) (JVM p.4).

Life cycle: at startup, native libraries, mapped JARs and threads go to the Native Heap; class metadata goes to PermGen; dynamic objects go to the heap. What is no longer used is returned by GC (JVM p.4).

### 2.2 Other JVMs

- **IBM JVM**: heap split into nursery and tenured, plus Native Heap; no PermGen (class metadata goes to the Native Heap). The `-Xgcpolicy:gencon` policy (concurrent and generational) is cited as typical of Java EE for reducing pauses (JVM p.6).
- **Oracle JRockit**: heap (young and old) plus native memory (classes, C-Heap, threads); no PermGen; on 32-bit the native space is between 2 and 4 GB minus the heap (JVM p.7). It only compiles, so the process tends to be about two hundred MB larger than the Sun equivalent, and the risk of native OOM is higher with a large heap on 32-bit (JVM p.8). The text mentions an Oracle plan to merge HotSpot and JRockit and does not report the outcome (JVM p.8). DATED.
- Wrong tuning often comes from ignoring the naming differences between JVMs (JVM p.5, p.8).

### 2.3 32-bit limit

On 32-bit, heap and native memory compete for the same address space: a larger heap leaves less for C-Heap and threads, and 2.5 GB or more of heap raises the risk of native OOM (JVM p.9). The theoretical process ceiling is 4 GB, possibly 2 GB on some older 32-bit Windows; on Solaris the text mentions native allocation failures near 3.5 GB (JVM p.88–90). On 64-bit the limit becomes physical memory, virtual memory and swap, plus the GC cost (JVM p.9, p.90). The author sums up that bigger is not always better ("bigger is not always the better") and advises against 20 Java EE applications in a single 16 GB process (JVM p.9).

### 2.4 Generations, sizing and major collection

- Pressure per region (author's heuristic) (JVM p.10): the number of applications in the process pressures the native heap; the number of classes and class loaders pressures PermGen and JIT objects; data caches pressure OldGen; the number of threads the middleware is allowed pressures native memory.
- The **static** footprint (classes, caches, applications) is predictable; the **dynamic** one comes from traffic (JVM p.11).
- Typical YoungGen:OldGen ratio cited as 1:3 ("33%"); 2 GB example on 32-bit: about 500 MB young and 1.5 GB old (JVM p.11). The numbers do not match (section 6.3).
- Large, non-serialized sessions demand a lot of OldGen; stateless XML-heavy applications, with many short-lived objects, demand an adequate YoungGen to reduce Full GCs (JVM p.11).
- Reducing the frequency of major collection is a key factor. The author's rule of thumb: up to about 50% heap occupancy after a major, to keep Full GC frequency low and leave headroom for failover; it is given in the example of a 64-bit VM with a 3 GB heap (JVM p.12). Minimizing major collections as a key factor is stated on p.11. OldGen at 80% or more with frequent GCs does not support failover: when instances are lost, the redirected load takes down the rest (JVM p.13).

### 2.5 Short-lived retention by threads

The thread stack holds the calls; the objects they create live on the heap (JVM p.15). Objects that should be short-lived (XML or JSON payloads) are retained by slow threads (lock, giant payload, slow remote system), get promoted to OldGen, increase Full GCs and can cause "OutOfMemoryError: Java heap space" without a real leak (JVM p.14–15). Increasing the thread stack does not reduce this retention; the adjustment applies to `StackOverflowError` and to the native-thread OOM. The stack-size flag is not named (JVM p.15, p.93).

### 2.6 PermGen and Metaspace as the text treats them

- **PermGen (JDK 7 and earlier)**: exhaustion produces "java.lang.OutOfMemoryError: PermGen space". The literal message string appears in the text only on p.22, when it says it ceases to exist with Metaspace; the PermGen OOM patterns (JVM p.85–86) speak of "PermGen space depletion" without reproducing the message, and the link between the message and that exhaustion is a reading of the whole. PermGen is exclusive to HotSpot (section 2.2). DATED.
- **Metaspace, treated as the future (Java 8 beta, build b75)**: the text says Java 8 would remove PermGen entirely (announced since JDK 7) and that interned strings already left PermGen in JDK 7 (JVM p.21). Class metadata comes to live in native memory, as already happened in JRockit and IBM (JVM p.22); `PermSize` and `MaxPermSize` are ignored with a warning if present at startup; `MaxMetaspaceSize` limits usage, and without it the space resizes itself (JVM p.22). GC of dead classes and loaders triggers when the limit is reached; excessive Metaspace GC may indicate a class or loader leak, or inadequate sizing (JVM p.22). Miscellaneous data were moved to the heap, and the text predicts more heap usage after upgrading to JDK 8 (JVM p.22–23).
- Removing PermGen does not eliminate class and class loader leaks; it changes the approach and the terminology (JVM p.22).
- Experiment (program that leaks classes, 1024 MB heap): JDK 1.7 with `-XX:MaxPermSize=128m` exhausted at about 30 thousand classes (JVM p.23). JDK 1.8 b75 with no limit: Metaspace from about 20 MB to about 328 MB reserved, with GCs of dead classes, and the 50 thousand iterations completed (JVM p.25). With `-XX:MaxMetaspaceSize=128m`: exhausted at about 30 thousand classes with a new OOM thrown by the JVM from the Metaspace after an allocation failure ("The above OOM event was thrown by the JVM from the Metaspace"), and the reserved native memory reached about double the maximum, which the author sees as an opportunity to tune the resizing policy (JVM p.25–26). The origin of the OOM in Metaspace is stated in text; the exact error message is not in the extracted text (whether it would be in an output shown as a figure, the extract does not tell).
- In b75, Metaspace usage appeared in the HotSpot 1.8 verbose GC; `jstat` and JVisualVM still showed references to PermGen (JVM p.23). DEPENDS ON VERSION: beta build; the text does not cover the final Metaspace.

### 2.7 Threads and native memory

Creating a Java thread creates a native thread, with a stack reserved in the process's native space. The OS refuses when the 32-bit addressing runs out (2, 3 or 4 GB) or when virtual memory runs out; on Solaris, lack of swap can cause SIGBUS on stack access and bring the JVM down (JVM p.90). Native OOM is usually a symptom of too many threads on "unhappy" paths (JVM p.92). JVM internal threads (GC threads, VM Thread, VM Periodic Task Thread) coexist with the container's; with the parallel collector HotSpot creates N GC threads, trading GC time for CPU (JVM p.41, p.45).

### 2.8 GC: what the text states

The text treats GC through occupancy per region (3.13), Full GC frequency and GC overhead limit (3.5). The labels `PSYoungGen`, `PSOldGen`, `PSPermGen` and the "ParallelGC" threads appear in the examples (PS* labels in JVM p.36–37, p.43 and p.46; "ParallelGC" threads on p.45); the text does not associate them by name with a collector, so saying "this is the Parallel GC" is an [inference]. CMS, G1, Serial and ParNew are not covered; the text does not cover collectors beyond this.

### 2.9 Class loaders

A class loader locates or generates the definition of a class. By the delegation pattern, each loader consults its parent before searching on its own, up to the bootstrap (JVM p.104); the parent does not see the children (JVM p.120). Chain in the example: bootstrap → `sun.misc.Launcher$ExtClassLoader` (`<JAVA_HOME>/lib/ext` or `java.ext.dirs`) → `sun.misc.Launcher$AppClassLoader` (startup classpath) → children such as `URLClassLoader` (JVM p.112, p.124). DATED: `sun.misc.Launcher` names. Containers such as WebLogic can override delegation (JVM p.105). A `static {}` runs once, at class load, in a thread-safe way (JVM p.103, p.112–113); if it fails, the class stays unusable until fixed and the JVM is restarted (or a live redeploy) (JVM p.103).

---

## 3. Diagnostic procedures

### 3.1 Triage by message or symptom

| Message or symptom | Points to | First step according to the text | Section |
|---|---|---|---|
| `OutOfMemoryError: Java heap space` | Allocation failure in the Java Heap | Verbose GC, OldGen trend, thread dumps, heap dump | 3.2, 3.3 |
| `OutOfMemoryError: PermGen space` | PermGen exhaustion, exclusive to HotSpot (IBM and JRockit have no PermGen, JVM p.5–7) (DATED) | Confirm the JVM is HotSpot; distinguish 3 patterns | 3.6 |
| `OutOfMemoryError: GC overhead limit exceeded` | Heap or tuning symptom | Verbose GC, OldGen trend, heap dump | 3.5 |
| `OutOfMemoryError: ... Out of swap space?` | Native memory (C-Heap or OS) | Do not increase `-Xmx`; measure process and OS | 3.7 |
| `OutOfMemoryError: unable to create new native thread` | Too many threads versus native memory or OS | Count threads, process size, 32 or 64 bits | 3.8 |
| `SocketException: Too many open files` | File descriptor limit | Capacity versus process usage | 3.10 |
| High CPU | Application or GC thread | CPU per thread in the OS, cross with dump | 3.9 |
| `[STUCK]` threads, hang | Deadlock, remote IO or resource deadlock | Thread dump, and several over time | 3.11, 3.12 |
| `ClassNotFoundException`, `NoClassDefFoundError` | Class loading | Class, caller, packaging | 3.14 |

### 3.2 OutOfMemoryError: Java heap space (JVM p.86–87)

- **Symptom**: message in the middleware logs (JVM p.86).
- **Possible causes**: heap too small for the traffic and footprint; leak in the heap (OldGen growing slowly); "rogue" thread consuming a lot in a short time (JVM p.86). Another cause, without a leak, is retention by threads (3.3).
- **Investigation**: (1) enable verbose GC with `-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -Xloggc:<caminho>/gc.log` (JVM p.86); (2) determine the YoungGen and OldGen footprint (JVM p.87); (3) follow the OldGen trend, via verbose GC or JConsole; (4) take thread dumps regularly, especially at jumps in heap usage, to find long-running threads that allocate heavily; (5) enable heap dump on OOM and analyze the HPROF with MAT (JVM p.87). The flag appears spelled inconsistently on that page (section 4.3).
- **Fix**: increase the heap (`-Xms`, `-Xmx`), reduce the footprint or eliminate leaks. Leaks also exist in middleware and in the JDK (JVM p.87).

### 3.3 Full heap without a leak: memory retained by threads (JVM p.14–21)

WebLogic 10.0 case after an interface change (GWT and JSON):

- **Symptom**: severe degradation, repeated "OutOfMemoryError: Java heap space", excessive GC; automatic heap dumps; verbose GC with the 1 GB OldGen (32-bit) exhausted; only a restart relieved it; the rollback fixed it (JVM p.16). The initial hypothesis, a leak in the new code, was wrong.
- **Investigation**: (1) thread dumps looking for STUCK threads; the OOM correlated with threads flagged by WebLogic (BEA-000337, 672 s against a 600 s limit) reading JSON from a remote server (JVM p.16–18); (2) in MAT, histogram filtered by `ExecuteThread`: 210 threads retaining 806 MB, a lot for a 1 GB OldGen (JVM p.18–19); (3) List objects, with outgoing references, and inspection of local variables of samples (JVM p.19–20). **Root cause**: huge JSON payloads (45 MB or more) in thread local variables (JVM p.20–21).
- **Cautions**: short-lived objects in local variables show up in the heap dump, and some are visible only from the owning thread; confirm with the stack trace and code review (JVM p.21).
- **Fix**: rollback; the delivery team located the changes that generated giant JSON; the text stresses capacity planning and analysis of memory retained by threads (JVM p.16, p.21).
- **Lesson**: before increasing the heap or hunting for a leak, look at the threads' execution pattern and how much each one retains (JVM p.15).

### 3.4 Heap dump: obtaining and analyzing; confirmed leak (JVM p.26–33)

**Obtaining**:

- Automatic on OOM, with the heap dump flag in the startup arguments on HotSpot 1.5, 1.6 and 1.7 (JVM p.28); the `.hprof` file (example `java_pid3880.hprof`) is written by the JVM (JVM p.64). The format is binary HPROF (JVM p.87).
- Manual with `jmap`: `<JDK HOME>/bin/jmap -heap:format=b <Java VM PID>` (the text's spelling, JVM p.28; it must be checked against the tool's help on the JVM in use, since the book offers no other form). The JVM is unresponsive during generation, so divert traffic beforehand; in the case, about 2 GB and about 1 hour (JVM p.28).

**Analyzing**: MAT is free (JVM p.87); the text calls it Eclipse MAT (JVM p.12, 26) and uses it via IBM Support Assistant (JVM p.27, 60). Features cited: histogram and filter by class; List objects, with outgoing references (what the class retains); with incoming references (who keeps it alive); Leak Suspects report; class loader data (JVM p.12–13, p.18–19, p.28–32, p.60). Jhat is the cited alternative (JVM p.60). Loading takes minutes, depending on size (JVM p.28).

**Real leak case (WebLogic 9.2, HotSpot 1.5.0_22, Solaris 10)**: (1) confirm the leak by the continuous growth of occupancy (Quest Foglight in the case; without a tool, enable `verbose:gc`) (JVM p.27); (2) generate the dump; (3) open it in MAT, starting with the histogram (JVM p.30); (4) the leaking objects were `java.lang.String` and `char[]`, and incoming references led to `javax.management.ObjectName` (JVM p.31–32); (5) the Admin Server collects statistics from the managed servers via MBeans/JMX, with one ObjectName per MBean; the cause was a known bug (CR327368, ObjectName leak in the WLS 9.2 Admin Server, fixed in WLS 10 MP1). The evidence combined dump, product version and bug description (JVM p.32–33).

**Not every heap OOM is a leak, and leaks are not only in the application code**: the handbook warns that leaks are frequent in middleware code and in the JDK (JVM p.87). For a full heap without a leak (threads retaining payloads), the pair is the thread dump with STUCK threads (JVM p.16–18) plus the heap dump with a histogram filtered by `ExecuteThread` and outgoing references (JVM p.18–21): the correlation between the two pieces of evidence is what locates the cause (JVM p.20). Increasing the thread stack does not help in this case (JVM p.15). Section 3.3.

### 3.5 OutOfMemoryError: GC overhead limit exceeded (JVM p.58–69)

- **What it is**: default policy presented as new in HotSpot 1.6; it detects an OOM condition before exhaustion and aborts the processing of the current threads. Rule cited: more than 98% of the time in GC and less than 2% of the heap recovered (JVM p.59). DEPENDS ON VERSION.
- **Usefulness according to the author**: avoids a total hang and gives the chance to collect dumps before the JVM becomes unreachable; it does not fix the heap (JVM p.59). In applications with occasional large allocations or long GC with healthy memory, it may cause more frequent OOMs; there the text suggests considering turning it off and observing (JVM p.59).
- **Turning off**: `-XX:-UseGCOverheadLimit` (JVM p.59–60). The error is very likely a heap or tuning symptom; focus on the root cause (JVM p.60).
- **Attacking it** (JVM p.60): `-verbose:gc`; analyze footprint and YoungGen/OldGen ratio (high OldGen leads to frequent Full GCs and the error); see whether OldGen grows over time (leak); consider the YoungGen if there are many short-lived objects; if a leak or high OldGen is suspected, use the heap dump flag and analyze with MAT or Jhat.
- **Tutorial** (JVM p.60–69): a simulator inserts Strings of about 1 KB (500,000 iterations) into a static HashMap until it blows up. Steps: maximum heap of 512 MB and the heap dump flag (JVM p.63); run (5 to 30 s); the JVM writes the `.hprof` (JVM p.64); open in MAT, which easily identified the static map (JVM p.64–69). Environment: Eclipse Indigo, MAT via ISA 4.1, 64-bit JRE 1.6.0_24 on Windows (JVM p.60). The screenshots of steps 3 and 4 were not extracted.

### 3.6 PermGen OutOfMemoryError: three patterns (JVM p.85–86) — DATED

**Only valid for HotSpot.** PermGen is exclusive to HotSpot: the IBM JVM and Oracle JRockit have no PermGen and use native memory for class metadata (JVM p.5–7). The text itself delimits the section to "PermGen space depletion of a Java HotSpot VM" (JVM p.85). Confirm the JVM vendor before applying `-XX:MaxPermSize` or any row of the table; on IBM or JRockit, the class metadata OOM would follow the Native Heap path (section 3.7), which is an [inference] from p.6, p.7 and p.22.

| Pattern | Symptoms | Probable cause | Resolution according to the text |
|---|---|---|---|
| After migrating the Java EE server to a newer version | OOM at start-up or at deploy; or after 1 to 2 hours or more of traffic | The new version requires more PermGen | Increase with `-XX:MaxPermSize` |
| After days | PermGen rises hour by hour or day by day | PermGen leak, most commonly a class loader leak; or arguments such as `-Xnoclassgc` | Review startup arguments; look for a class loader leak in the heap dump; investigate third-party APIs, Reflection and dynamic loading |
| After redeploy (EAR, WAR) | OOM during or right after | Unloading and reloading code leaks PermGen | Ticket to the Java EE vendor (known leak); restart the JVM after the deploy |

For JVMs without PermGen, the text only offers the Metaspace mapping from section 2.6 (beta).

### 3.7 OutOfMemoryError: Out of swap space (native memory) (JVM p.87–92)

- **Definition**: thrown by HotSpot's native code when native memory allocation fails, either for the C-Heap or to expand the Java Heap; it differs from the ordinary heap or PermGen OOM (JVM p.87–88).
- **Symptom**: message of the type "requested N bytes for ChunkPool::allocate. Out of swap space?" (JVM p.87). On Windows, AIX and Solaris the C-Heap OOM may come without this text; read the stack trace and the task that triggered it to classify among Java Heap, PermGen and Native Heap (JVM p.88).
- **Do not**: increase `-Xms` or `-Xmx`; the text says it is the last thing to try, since on 32-bit it makes things worse (JVM p.88). First, determine whether what is exhausted is the C-Heap or the OS.
- **Patterns** (JVM p.88): many applications in a 32-bit JVM with a large heap (the most common, according to the author); heap too large on 32-bit; too many container threads; OS out of memory to allocate C-Heap (32 or 64 bits); OS out of memory to expand heap or PermGen; native leak (third-party monitoring agent, library, JVM bug).
- **Investigation** (JVM p.88–89): monitor OS memory and process size (growth over days reveals a native leak); check the OS and the process limit; see whether the JVM is 32 or 64 bits (on 64, it is usually lack of memory in the OS); on 32-bit, a heap of 2 GB or more already pressures the C-Heap, and the text suggests evaluating a reduction of about 256 MB as a starting point, using verbose GC or JConsole to know whether it is safe; take a thread dump at the moment of the OOM and count threads.
- **Fixes** (JVM p.89): reduce the heap after monitoring; increase RAM or virtual memory; migrate to 64-bit or segregate applications into more JVMs (more hardware, less C-Heap per JVM); for a native leak, `pmap` (Solaris) or `svmon` (AIX), review of third-party libraries and consultation of the Oracle/Sun bug database for the version.
- **Example fatal crash** (JVM p.91–92): on Solaris, lack of virtual memory and swap brought the JVM down with the report "A fatal error has been detected by the Java Runtime Environment", citing `ChunkPool::allocate` (`allocation.cpp:166`), JRE 6.0_24-b07, HotSpot Server VM 19.1-b02, solaris-sparc, thread `CompilerThread1`.

### 3.8 OutOfMemoryError: unable to create new native thread (JVM p.89–93)

- **Definition**: the JVM's native code could not create a native thread in the OS; the error does not detail the reason. The section title is at the end of p.89 and the explanation on p.90, which also says the problem is usually tied to native memory exhaustion, in the process or in the OS (JVM p.89–90).
- **Collect before concluding** (JVM p.91): JVM 32 or 64 bits; thread dump at the moment (how many threads); process size before and during; OS virtual memory (swap, on Solaris).
- **Patterns** (JVM p.91–92): (1) C-Heap exhausted on 32-bit by too many threads; (2) OS virtual memory exhausted on 64-bit, by a few large processes (10 GB or more) and/or other "rogue" processes; (3) OS virtual memory exhausted on 32-bit (less frequent; the JVM may be the source or the victim; may bring the JVM down on Solaris).
- **Symptom versus cause**: the mandatory question is how many threads were active. From the author's experience, the most common cause is the application or container creating too many threads on "unhappy" paths (stuck remote IO, race conditions). Before more memory or migrating to 64-bit, understand the root cause (JVM p.92).
- **Recommendations** (JVM p.93): rule out obvious OS and limit problems (`ulimit`); compare the thread dump with a baseline to find the origin of the threads; monitor process and virtual memory; look at all processes (is the JVM the source or the victim?); review the container's thread configuration and the JVM stack size; if the 32-bit heap is in the way, reduce it, scale vertically or migrate to 64-bit. Load tests must measure container threads and native memory, including unhappy paths.

### 3.9 High CPU: finding the culprit thread (Windows) (JVM p.49–54)

1. Use Process Explorer; for per-thread history, `perfmon` with % Processor Time and Thread Id (JVM p.52).
2. Identify the Java process (example: Eclipse's `javaw.exe`, about 25% CPU); Properties, Threads tab (JVM p.52).
3. The view shows Thread Id in decimal and CPU %; in the example, thread 5996 with about 25% (JVM p.53).
4. Take a thread dump (in the example, JRockit with `jrcmd`; exact command in a figure) and look for the id (JVM p.53–54).
5. Read the stack trace: in the example, `HighCPUSimulator.main`, line 31 (artificial loop). The real cause can range from a simple loop to GC problems (JVM p.54).

ID trap: in the HotSpot dump the `nid=` is in hexadecimal (example `nid=0x251c`) (JVM p.42), whereas Process Explorer shows decimal (JVM p.53). The example uses JRockit, where `tid=5996` matches the decimal (JVM p.54). The text does not describe the decimal to hexadecimal conversion on HotSpot; [inference] it is necessary, but not made explicit. On Solaris, the text cites `prstat` for the native id (JVM p.45). If the busiest thread is a GC thread, it appears by native id (example `nid=0x3`, "GC task thread#0 (ParallelGC)") and the topic becomes GC sizing and frequency (JVM p.45).

### 3.10 "Too many open files" (file descriptors) (JVM p.54–58)

- **Context**: Oracle Service Bus 11g on IBM AIX 6.1, 64-bit IBM JRE 1.6.0 SR9, after migrating from ALSB 2.6 on Solaris (JVM p.54–55).
- **Symptom**: `java.net.SocketException: Too many open files` under load; managed servers hang; WebLogic closes the HTTP port and stops responding; restart helps only for a while (JVM p.55). High impact, recent change (migration), no traffic increase: load-related problem.
- **Why it matters**: the error affects the whole process; FDs are also consumed by sockets, and the limit must cover peaks and slowness of external systems (JVM p.55–56).
- **Investigation (AIX, JVM p.56)**: `procfiles <PID> | grep rlimit`, `lsof -p <PID> | wc -l`, `ulimit -S -n`. In the case: limit 2000, 1920 FDs in use, `ulimit -S -n` 2000, i.e. near the ceiling (JVM p.56–57).
- **Root cause**: the WebLogic script that overrides the limit at startup (`<WL_HOME>/wlserver_10.3/common/bin/commEnv.sh`) only applied the `ulimit` on Solaris; on AIX the default 2000 remained, against 65536 of ALSB 2.6 on Solaris (JVM p.57).
- **Fix**: adjust commEnv to apply 65536 on AIX too (excerpt in a figure, not extracted); takes effect only after restarting Node Manager and managed servers; validated with `procfiles` (JVM p.57–58). When upgrading the container, check the FD limit and monitor FDs to anticipate capacity or a socket leak (JVM p.58).

### 3.11 Thread dump: obtaining, reading and interpreting states (JVM p.40–49)

**Obtaining**: Unix `kill -3 <PID>` (standard output or process log) (JVM p.44, p.70); JVisualVM and `jstack` (JVM p.70); IBM, javacore (JVM p.74); JRockit, `jrcmd` (JVM p.53).

**Anatomy (HotSpot)** (JVM p.42): name, type and priority, `tid=` (Java id), `nid=` (native id, basis for cross-referencing with OS CPU), state and stack trace (about 90% of the information). Since HotSpot 1.6, a heap summary at the end. Example header: `Full thread dump Java HotSpot(TM) 64-Bit Server VM (20.0-b11 mixed mode)` (JVM p.44). The heap summary confirms or rules out GC pressure in a single capture; in the example, OldGen at 99% and PermGen at 94% (JVM p.43, p.46).

**Stack reading script, bottom to top** (JVM p.47–48): (1) at the base, the origin (container thread, custom, GC, internal JVM or `main`); (2) the request type (WebApp, Web Service, JMS, RMI, internal); (3) the application modules involved; (4) the last 10 to 20 lines before the top, to see the protocol or work (HTTP, socket, JDBC, disk, class loading); (5) the first line, what was executing at that instant; (6) 4 and 5 together reveal the work or the hang condition.

**Categories in a container dump** (JVM p.47–48): computing (XML parse, disk); waiting on blocking IO (web service, JDBC); GC; waiting for work (`wait()`); waiting on a monitor (`synchronized`). Idle WebLogic pool thread: `[STANDBY] ExecuteThread` in `WAITING (on object monitor)`, in `waitForRequest` (JVM p.45). "Thread created" is not "thread working" (JVM p.47). Creating threads in application code is seen as bad practice (JVM p.45). A pattern of excessive IO repeated across several threads appears in the JBoss 5 case with JAX-WS (JVM p.48).

**States**: in the pages covered there is no formal table of states. What the text gives is piecemeal: `WAITING (on object monitor)` for idle ones (JVM p.45); "waiting to lock" and `locked <0x...>` for monitors (JVM p.84); `Unsafe.park` and `AbstractQueuedSynchronizer` for waiting on `java.util.concurrent` locks (JVM p.84); state `B` (blocked) in the IBM format (JVM p.76–78); and the warning that a thread may appear RUNNING even when hung ("RUNNING state != healthy state") (JVM p.72). A complete table of states would be external knowledge and is not provided.

**Global JNI references**: the dump shows the count (1925 in the example); they prevent collection of objects used by native code, and tracking them helps detect JNI leaks, in own code or in third-party agents (JVM p.46).

### 3.12 Deadlock, stuck threads and resource deadlock

**Definition**: permanent blocking of threads waiting for each other, distinct from contention, race or IO wait (JVM p.69, p.75). Two types: lock-ordering (different acquisition orders; only a restart recovers) and resource deadlock (waiting for a resource never released, such as an exhausted JDBC pool) (JVM p.70, p.72). The author says resource deadlock is the most common and is not a true Java deadlock; true deadlocks are rare (about 5 in 10 years) and most "stuck" cases are remote IO waits (JVM p.74). The "golden rule" for stuck threads is to take the thread dump (JVM p.73–74).

**Native detection**: HotSpot and IBM dumps list Java-level deadlocked threads with their stacks (JVM p.70). On HotSpot the section appears as "Found one Java-level deadlock" (JVM p.79, 83). In the IBM javacore, the section starts at `1LKDEADLOCK Deadlock detected !!!`, with each thread, the monitor it waits for and the current owner (JVM p.73–74). Procedure: confirm the deadlock, read the partial stack of each thread (task and wait condition), identify the contended resource, review code and search the bug tracker of the suspect framework (JVM p.75–78). The culprit code is usually a third-party API or the container, except in high-concurrency programming (JVM p.71).

**Resolution** (from the cited talk "HOL6500" by Heinz) (JVM p.71–72): (1) global lock ordering; (2) `tryLock` with `Lock`/`ReentrantLock` and timeout, waiting and retrying if the second lock fails (the text cites JBoss AS7 as an extensive user); (3) always release in `finally`, otherwise the deadlock becomes a livelock.

**Resource deadlock** (JVM p.72): the dump does not report a deadlock. Collect several dumps over time and see which threads do not move (those waiting for the resource and those that obtained it and are hung); do not trust the thread state; cross with resource statistics and middleware health. The fix depends on the cause and may not require a code change.

**"Hidden" deadlock with a read lock** (JVM p.79–85) — DEPENDS ON VERSION (the text attributes it to HotSpot 1.7):

- **Symptom**: hung threads, and from the stacks two are clearly in deadlock, but the dump does not show the Java-level section (JVM p.82). The absence of the message does not prove there is no deadlock (JVM p.79).
- **Pattern**: path 1 with a plain lock (`synchronized`) and then the write lock of a `ReentrantReadWriteLock`; path 2 with the read lock and then the plain lock; two threads in inverted orders (JVM p.79–81).
- **Cause**: read locks have no notion of owner by design; without a record of which thread holds them, the detector does not see the cycle (JVM p.83). Write locks are tracked like plain locks (JVM p.84). Swapping the read lock for a write lock, the JVM detects it and lists "waiting for ownable synchronizer" of `ReentrantReadWriteLock$NonfairSync` (JVM p.83–84). The text cites a 2005 comment by Doug Lea about the cost of tracking read holds (JVM p.84).
- **Investigation** (author's recommendations, JVM p.85): closely analyze the threads' call stack, which may reveal code that acquires read locks and prevents other threads from acquiring write locks; and, if the code is yours, track the read lock count with `lock.getReadLockCount()`. The experiment's dump was generated with JVisualVM and does not include the "Found one Java-level deadlock" section (JVM p.82).
- **Stack pattern, synthesis [inference]**: the textual stack listing on p.84 belongs to the scenario in which the read lock was swapped for a write lock, in which case the JVM detects the deadlock and prints "Found one Java-level deadlock" (JVM p.83); the dump of the undetected scenario is in an image (p.82), not extracted. The listing on p.84 shows `pool-1-thread-2` in `Unsafe.park`/`AbstractQueuedSynchronizer` waiting on `ReentrantReadWriteLock$WriteLock.lock` with `locked <0x272236d0>`, and `pool-1-thread-1` "waiting to lock" the same monitor. That the hidden case, with a read lock, shows the same stack pattern is my deduction; the book does not state it.
- **Fix**: the text only diagnoses. That the order inversion must be eliminated is an [inference], not a literal recommendation (JVM p.80).
- **Author's methodology**: treat it as a crime scene; collect evidence (dump, logs, impact, load), listen to experts (support, delivery, vendor, customer), list suspects and proofs and narrow down (JVM p.79).

### 3.13 Reading verbose GC output (HotSpot Java 7 build 21.0-b17) (JVM p.33–39)

- **Setup**: program that fills a static HashMap with about 3 million Strings, calls `System.gc()`, removes 2 million and calls `System.gc()` again (JVM p.33–34). Enable verbose GC in the startup arguments, with output to a file; the exact arguments were in a figure and were not extracted (JVM p.35).
- **Log structure** (JVM p.36–37): minor collections labeled `PSYoungGen`; major collections (here from `System.gc()`) labeled `Full GC (System)`; and a heap breakdown by space (eden, from, to; PSOldGen; PSPermGen).
- **Reading the example** (JVM p.37–38): a minor collection shows YoungGen in the format before→after(capacity), then the total heap in the same format, with time and a Times line (user, sys, real). Example: YoungGen 262208K→43632K(305856K), heap 262208K→137900K(1004928K), 0.14 s. OldGen went to 340 MB with 3M Strings and to 126 MB after removing 2M and running Full GC. The Full GC reports `PSPermGen` (1554K→1554K(16384K)). In a parallel collection, `user` may exceed `real` (user=0.45, real=0.14); this is a reading of the sample, not commented on by the text. The before→after(capacity) format is an interpretation of the sample, since the explanatory figures (JVM p.38–39) were not extracted.
- **Use**: OldGen trend after majors (growing indicates a leak), Full GC frequency and young/old ratio; the author's target of about 50% post-major (JVM p.12).

### 3.14 ClassNotFoundException and NoClassDefFoundError (JVM p.93–126)

**ClassNotFoundException**: class loading failure by name (`Class.forName`, `ClassLoader.loadClass`, `findSystemClass`) (JVM p.93). It generally comes from an API that references the class, not from the application code; another pattern is wrong packaging (JVM p.94). Reproduction: replacing the target class with a non-existent one fails the same way on both paths, with the stack in `URLClassLoader.findClass` and `AppClassLoader.loadClass` (JVM p.95–98). Strategy (JVM p.98–99): rule out simple causes; read the stack to know which class failed; identify the caller (the class right before `forName()`/`loadClass()`); check the packaging; if it is third-party, add the JAR to the classpath or to the WAR/EAR; if it persists, suspect the loader hierarchy.

**NoClassDefFoundError**: the JVM tries to load the definition and does not find it in the loader tree; the reference compiled but does not exist at runtime (JVM p.99, p.103). It usually comes with `Caused by: ClassNotFoundException` (JVM p.111, p.125). Three patterns:

1. **Missing JAR** (JVM p.102, p.111–112): identify the class; find in the build the JAR that contains it; compare the build classpath with the production one; add the JAR to the system classpath or to the EAR. Most common with container and third-party JARs (Apache, Spring, Hibernate). In Java EE, check dependency JARs and MANIFEST (JVM p.112). **Incompatible version** variant (less common, JVM p.102): identify the missing class and the referencer (the text emphasizes this), find both JARs in the build, compare with production and replace with the correct version, which may include the referencer's JAR.
2. **Failure in `static {}` or static variable** (JVM p.102–103, p.113–119): the first use throws `ExceptionInInitializerError`; subsequent ones throw `NoClassDefFoundError: Could not initialize class <X>`, consistently. The `NoClassDefFoundError` is only a symptom; look in the log for the first error, not the last. Investigate: identify the class, look for static initialization in the code, review logs for the `ExceptionInInitializerError`. Fix: `try/catch` and logging in the initializer, compile, redeploy, retest; recovery requires restarting the JVM or a live redeploy (JVM p.103, p.119). The output labeled "static variable initializer failure" on p.116 shows execution without error (probable PDF shuffling); the real error is on p.117–118.
3. **Duplication between parent and child loader (parent-first)** (JVM p.119–126): the caller's JAR is in both the parent and the child; by delegation it loads through the parent, which does not see `ReferencingClassA`, present only in the child. Contributing factor: JAR injection by the container or by third parties at a high level of the chain (JVM p.119, p.126). Investigate (JVM p.126): identify the class; review the packaging (system classpath, EAR, container) for duplicate deployment; use `-verbose:class` to find duplicate loading. Fix: remove or move the libraries from the wrong loader. Tip: print the loader chain and `CLAZZ.getClassLoader()` in the static initializer (JVM p.96, p.105–109). Caution: the text states that, when the class is not found in the parents, the JVM tries the thread's context loader (JVM p.119), but in the example the load through the child is an explicit call (JVM p.121); do not generalize it as a rule.

### 3.15 Heap sizing and number of JVMs (JVM p.8–14)

1. Understand the memory spaces before touching flags; anti-pattern: copying `-Xms`/`-Xmx` from another OOM case, and the problem returns in days (JVM p.8–9).
2. Estimate the static and dynamic footprint (JVM p.10–11). Example: 5 EARs (about 2 thousand classes), 1 GB native heap, 512 MB PermGen, 500 MB cache and 5,000 users × 500 KB of session = 2.5 GB of session alone; unfeasible in a 32-bit process, suggesting splitting the traffic and/or 64-bit with a 3 GB heap to contain the GC cost (JVM p.11–12).
3. Author's starting points: 32-bit with up to 2 GB (`-Xms2048m -Xmx2048m`); 64-bit with 3 to 4 GB per process (JVM p.11).
4. Measure: profiler (JProfiler), heap dump with MAT, load test (Apache JMeter), including simulating failover (JVM p.12–14).
5. If there is no leak and the footprint does not shrink, create more JVM processes per host and across hosts: smaller heap per process, simpler tuning, less GC pause, more redundancy, at the cost of more hardware (JVM p.14).

---

## 4. Flags and tools cited, with the text's version

### 4.1 Flags and options

| Flag/option | What it is for according to the text | Text's version | Page |
|---|---|---|---|
| `-Xmx` / `-Xms` | Maximum and minimum heap (example 1024m); also cited for IBM and JRockit | HotSpot, IBM, JRockit | JVM p.3, 6, 7, 87, 88, 90 |
| `-XX:MaxPermSize` / `-XX:PermSize` | Maximum and minimum PermGen size; remedy for PermGen OOM after migration | HotSpot up to JDK 7; DATED | JVM p.3–4, 22, 85, 90 |
| `-XX:MaxPermSize=128m` | Limit of the class-leaking test | JDK 1.7 | JVM p.23 |
| `-XX:MaxMetaspaceSize` | Limits native memory for class metadata (example 128m) | HotSpot 1.8 b75 (beta); DEPENDS ON VERSION | JVM p.22, 25–26 |
| `-Xgcpolicy:gencon` | IBM's concurrent and generational GC policy | IBM JVM | JVM p.6 |
| `-verbose:gc` | Enables verbose GC (also spelled `verbose:gc`) | HotSpot; tutorial on Java 7 | JVM p.27, 33, 60, 86 |
| `-XX:+PrintGCDetails`, `-XX:+PrintGCTimeStamps`, `-Xloggc:<caminho>/gc.log` | Detail the log, timestamp it and write to a file | HotSpot of the era | JVM p.86 |
| `-XX:+HeapDumpOnOutOfMemoryError` | Generates an HPROF heap dump on OOM | HotSpot 1.5, 1.6, 1.7 | JVM p.28, 60, 63 |
| `-XX:HeapDumpOnOutOfMemoryError` (without `+`) | Same purpose, divergent spelling | See 4.3 | JVM p.87 |
| `-XX:-UseGCOverheadLimit` | Turns off the GC overhead limit policy | HotSpot 1.6 | JVM p.59–60 |
| `-Xnoclassgc` | Turns off class GC; cited as an improper argument that contributes to exhausting PermGen | HotSpot; DATED | JVM p.85 |
| `-verbose:class` | Monitors class loading; helps find duplication | HotSpot | JVM p.126 |
| `java.ext.dirs` | `ExtClassLoader` directories | JDK of the era | JVM p.112 |
| Thread stack size | Relevant for `StackOverflowError` and native-thread OOM; flag not named | HotSpot | JVM p.15, 93 |
| `jmap -heap:format=b <PID>` | Generates a binary heap dump; syntax to be checked (4.3) | HotSpot 1.5 (cited) | JVM p.28 |
| `kill -3 <PID>` | Thread dump to the process output (Unix) | HotSpot | JVM p.44, 70 |

### 4.2 Tools

| Tool | What it is for according to the text | Text's version | Page |
|---|---|---|---|
| Eclipse Memory Analyzer (MAT), also via IBM Support Assistant | Analyze HPROF: histogram, incoming and outgoing references, Leak Suspects | MAT 1.1 (p.27), ISA 4.1 (p.60) | JVM p.12, 18–19, 27–32, 60, 87 |
| Jhat | Alternative to MAT | JDK of the era | JVM p.60 |
| `jmap` | Generate a heap dump (JVM unavailable during generation) | HotSpot 1.5 (case) | JVM p.28 |
| `jstack`, JVisualVM | Generate a thread dump | JDK of the era | JVM p.70, 82 |
| JConsole, JMX, JVisualVM | Monitor heap and trends | JDK of the era | JVM p.3, 23, 60, 87 |
| `jstat` | Statistics; in b75 it still showed references to PermGen | JDK 8 b75 | JVM p.23 |
| `jrcmd`, JRockit Mission Control | Operation and monitoring on JRockit (thread dump) | JRockit | JVM p.7, 53 |
| `prstat` | Native thread id (Solaris) | Solaris | JVM p.45 |
| `pmap`, `svmon` | Process native memory | Solaris, Linux, AIX | JVM p.4, 6, 89 |
| Process Explorer, `perfmon` | CPU per thread on Windows | 64-bit Windows 7 | JVM p.50, 52 |
| `procfiles`, `lsof`, `ulimit -S -n` | File descriptors (AIX) | AIX 6.1 | JVM p.56, 93 |
| javacore | IBM thread dump, `1LKDEADLOCK` section | IBM JRE 1.6.0 | JVM p.73–74 |
| `ReentrantReadWriteLock.getReadLockCount()` | Count read locks in own code | JDK 7 (examples) | JVM p.85 |
| JProfiler, Apache JMeter, Quest Foglight | Profile, load test and monitor in the cases | cited | JVM p.12–13, 27 |

### 4.3 Book discrepancies to record

- **Heap dump flag without the `+` sign.** In JVM p.87 the text writes `-XX:HeapDumpOnOutOfMemoryError`, without `+`. The occurrences on JVM p.28, 60 and 63 have `-XX:+HeapDumpOnOutOfMemoryError`. The form without `+` is divergent within the book itself; [inference] it is a spelling error on p.87. When citing the flag, use the form with `+` from p.28, 60 and 63 and check the syntax on the JVM in use; the text covers no more than that.
- **`jmap -heap:format=b`** (JVM p.28). The syntax is as the text gives it and must be checked against the tool's help on the target JVM; the book gives no other spelling to compare.
- **`verbose:gc` (JVM p.27) and `-verbose:gc` (p.33, 60, 86)**: [inference] same flag, with different spelling on p.27.

---

## 5. Case studies: what each one illustrates

- **WebLogic 10.0, giant JSON (JVM p.14–21)**: OOM without a real leak; heap retained by pool threads; MAT histogram filtered by `ExecuteThread`.
- **WebLogic 9.2, ObjectName (JVM p.26–33)**: real leak; incoming references; cause in a known vendor bug.
- **Verbose GC with 3M Strings (JVM p.33–39)**: reading of minor collections and `Full GC (System)`.
- **HighCPUSimulator (JVM p.49–54)**: from the highest-CPU thread in the OS to the stack trace; decimal versus hexadecimal.
- **OSB 11g on AIX (JVM p.54–58)**: default FD limit (2000) because the script only handled Solaris; migration hides implicit configurations.
- **JVMOutOfMemoryErrorSimulator (JVM p.60–69)**: automatic heap dump and leaking static map.
- **Deadlock on WebLogic 11g, Spring 2.0.5, AIX 5.3, IBM JRE 1.6.0 (JVM p.73–78)**: symptom (sudden increase and depletion of threads, STUCK on 2 of 16 managed servers, intermittent, after a change with asynchronous JMS; medium impact, no traffic increase, restart fixes it for hours) and detection of the deadlock between threads #8 and #10 (`FESession`, `FEConnection`) (JVM p.73–74). The continuation (JVM p.75–78) shows #8 in `SingleConnectionFactory.resetConnection` → `closeConnection` → `FEConnection.stop` and #10 in `JmsTemplate.receiveSelected` → `createConsumer` → `FEConnection.getPeerVersion`, both in state `B`. Cause: connection reset of Spring's `SingleConnectionFactory` without thread-safety, a known defect in Spring's JIRA. Fix: a 2009 patch with `synchronized` over a connection monitor and a check of the `started` flag; the team planned to apply it in production. Illustrates the cycle dump, shared resource, bug tracker.
- **Hidden deadlock in OSB (JVM p.79–85)**: reproduction with the `Task` class, which has two paths: `executeTask1` (read lock, waits 2 s, then `synchronized`) and `executeTask2` (`synchronized`, waits 2 s, then write lock), fired by two worker threads (JVM p.80–81); the name `WorkerThread2` appears only in a stack frame on p.84; the experiment's dump has no deadlock section (JVM p.82; the listing was not extracted). The stack listing on p.84, with `pool-1-thread-2` waiting in `WriteLock.lock` with `locked <0x272236d0>` and `pool-1-thread-1` "waiting to lock" the same monitor, is that of the write-lock scenario, in which the JVM detects the deadlock (JVM p.83–84); using it as a picture of the hidden case is an [inference]. The author's recommendations for the hidden case are to analyze the call stack and track `lock.getReadLockCount()` (JVM p.85). Illustrates the detector's limitation.
- **Crash from lack of virtual memory on Solaris (JVM p.91–92)**: native OOM can bring the process down.
- **PermGen versus Metaspace (JVM p.23–26)**: the same class-leaking program on JDK 1.7 and 1.8 b75.
- **Class loading simulators (JVM p.94–126)**: `ClassNotFoundException` with `ClassA`/`ClassB` (JVM p.95–98); missing JAR with `ClassC.jar` outside the classpath (JVM p.100–101, p.105–112); static initializer with `REPLICATE_PROBLEM1` (static variable) and `REPLICATE_PROBLEM2` (`static{}` block), one `ExceptionInInitializerError` and two `NoClassDefFoundError` (JVM p.113–119); parent-first with `caller.jar` in the parent and the child (JVM p.119–126).

---

## 6. Version assumptions of the text and gaps

### 6.1 Version assumptions of the text

- **HotSpot and Java**: GC overhead limit new in HotSpot 1.6 (JVM p.59); heap summary in the dump since 1.6 (JVM p.42, 46); HotSpot 1.5.0_22 (JVM p.27); automatic heap dump in 1.5 to 1.7 (JVM p.28); Java 7 build 21.0-b17 (JVM p.33); banner 20.0-b11 (JVM p.44); JRE 1.6.0_24 (JVM p.60); JDK 1.7 and 1.8 b75 (JVM p.21, 23); "latest HotSpot JVM 1.7" in deadlock detection (JVM p.79); JRE 6.0_24-b07 and Server VM 19.1-b02 (JVM p.92); `jdk7` package (JVM p.114).
- **Java 8 as the future**: PermGen removal and Metaspace are treated as under development; final specifications, flags and documentation would only come at release (JVM p.21–22). DATED and DEPENDS ON VERSION.
- **Other JVMs, middleware and OSes**: 64-bit IBM JRE 1.6.0 SR9 (JVM p.55) and 1.6.0 (JVM p.73); JRockit (JVM p.53); WebLogic 9.2 MP1, 10.0, 10.3, 11g; OSB 11g and ALSB 2.6; Solaris 10, AIX 5.3 and 6.1, 64-bit Windows 7; JBoss 5 and AS7; Spring 2.0.5; Eclipse Indigo; MAT 1.1 and ISA 4.1. The WebLogic example logs are from December 2012 (JVM p.17).
- **Architecture**: a 32-bit JVM with 2 to 4 GB per process is the central premise of the recommendations (JVM p.7, 9, 11, 88–90, 93).
- **Collectors**: the parallel collector appears ("ParallelGC" threads, `PS*` labels) (JVM p.36–37, 45), and IBM's `gencon` (JVM p.6). CMS, G1, Serial, ParNew, Java Flight Recorder and `jcmd` are not covered.
- **What changed after the text**: the text does not cover it. Default values, tool and flag availability, Metaspace OOM messages and `jmap` syntax must be verified in a current source. The JDK 11 to 26 release notes provided do not deal with these topics.
- **Author's rules, not official**: 2 GB on 32-bit and 3 to 4 GB on 64-bit (JVM p.11); about 50% post-major, in the example of a 64-bit VM with a 3 GB heap (JVM p.12); 256 MB reduction on 32-bit (JVM p.89). The "most common" claims reflect personal experience (JVM p.88, 92).

### 6.2 Gaps

- **Figures not extracted**: verbose GC arguments (JVM p.35) and per-space explanations (JVM p.38–39); `jrcmd` command (JVM p.53); `commEnv.sh` excerpt (JVM p.57–58); MAT screenshots in the tutorial (JVM p.64–69); pages 29, 65, 67 and 68 came out empty. Do not deduce these details. Separately, the exact Metaspace OOM message is not in the extracted text, although p.26 says in text that the OOM came from Metaspace.
- **Deadlock case cut off on p.74**: the WebLogic 11g case with IBM JRE starts at JVM p.73–74 and the analysis is left incomplete there; the continuation is at JVM p.75–78. That the two parts are the same case is an [inference] supported by threads #8 and #10 and the WebLogic JMS components.
- **J9VMThread**: the `J9VMThread` and `j9thread_t` headers of the dumps (JVM p.76–78) suggest the IBM J9 format, but the text, on those pages, does not name the vendor. Identifying it as IBM J9 is an [inference], reinforced by the start of the case stating IBM JRE 1.6.0 (JVM p.73) and javacore (JVM p.74).
- **Dump commands**: `jstack`, `jmap` and `kill -3` appear only in the first half (JVM p.28, 44, 70); the second cites JVisualVM and JConsole.
- **Fix for the read lock deadlock**: the text only diagnoses (JVM p.80, 85).
- **Frameworks**: Spring and Hibernate appear in the handbook only in case studies, not as a taught subject: Spring JMS's non-thread-safe `SingleConnectionFactory` as the cause of the deadlock (JVM p.78; Spring 2.0.5 on p.73), and Hibernate in a list of missing third-party libraries that cause `NoClassDefFoundError` (JVM p.102). Questions about configuring or using these frameworks have no basis in the sources.

### 6.3 Internal inconsistencies

- **YoungGen:OldGen ratio**: "1:3" and "33%" in the text, but 500 MB of 2 GB is 25% (JVM p.11). Treat as an order of magnitude.
- Heap dump flag with and without `+` (section 4.3); sentence about the context loader versus the example (section 3.14).
