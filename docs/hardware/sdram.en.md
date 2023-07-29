# SDRAM

## Features

SDRAM features:

1. low cost, each 1 bit cell requires only one CMOS transistor
2. complex interface, you need to activate a row before accessing data, and then read the data in the row
3. the controller is also complex and requires periodic memory refreshing
4. large capacity, because the row and column multiplexed address lines, a single memory module can achieve GB level capacity

## Standards

SDRAM-related standards are developed by JEDEC:

- [JESD79F: DDR SDRAM](https://www.jedec.org/standards-documents/docs/jesd-79f)
- [JESD79-2F: DDR2 SDRAM](https://www.jedec.org/sites/default/files/docs/JESD79-2F.pdf)
- [JESD79-3F: DDR3 SDRAM](https://www.jedec.org/sites/default/files/docs/JESD79-3F.pdf)
- [JESD79-4D: DDR4 SDRAM](https://www.jedec.org/document_search?search_api_views_fulltext=jesd79-4%20ddr4)
- [JESD79-5B: DDR5 SDRAM](https://www.jedec.org/document_search?search_api_views_fulltext=jesd79-5)

In addition to the DDR series, there is also a low-power LPDDR series:

- [JESD209B: LPDDR SDRAM](https://www.jedec.org/system/files/docs/JESD209B.pdf)
- [JESD209-2F: LPDDR2 SDRAM](https://www.jedec.org/system/files/docs/JESD209-2F.pdf)
- [JESD209-3C: LPDDR3 SDRAM](https://www.jedec.org/document_search?search_api_views_fulltext=JESD209-3)
- [JESD209-4D: LPDDR4 SDRAM](https://www.jedec.org/document_search?search_api_views_fulltext=JESD209-4)
- [JESD209-5B: LPDDR5 SDRAM](https://www.jedec.org/document_search?search_api_views_fulltext=JESD209-5)

High-performance HBM is also based on SDRAM technology:

- [JESD235D: HBM](https://www.jedec.org/standards-documents/docs/jesd235a)
- [JESD238A: HBM3](https://www.jedec.org/system/files/docs/JESD238A.pdf)

GDDR SGRAM series:

- [SDRAM3.11.5.8 R16.01: GDDR4 SGRAM](https://www.jedec.org/system/files/docs/3_11_5_8_R16.01.pdf)
- [JESD212C.01: GDDR5 SGRAM](https://www.jedec.org/system/files/docs/JESD212C.01.pdf)
- [JESD232A.01: GDDR5X SGRAM](https://www.jedec.org/system/files/docs/JESD232A.01.pdf)
- [JESD250D: GDDR6 SGRAM](https://www.jedec.org/system/files/docs/JESD250D.pdf)

The following is an introduction to DDR series SDRAM.

## Concepts

DDR SDRAM is often given a number to represent its performance, such as 2133 for DDR4-2133, and sometimes you will see the term 2400 MT/s. Both refer to the maximum number of data transfers per second that SDRAM can perform in millions of transfers per second. Since SDRAM uses DDR to transfer two copies of data per clock cycle, the actual clock frequency is divided by two, so 2133 MT/s corresponds to a clock frequency of 1066 MHz.

Sometimes you will also see PC4-21333 written to describe memory sticks, where $21333 = 8*2666$, which is 2666 MT/s, multiplied by 8 because the data bit width of a DDR memory module is 64 bits, so the theoretical memory bandwidth of a 2666 MT/s memory stick is $2666 \mathrm{(MT/s)} * 64 \mathrm{(bits)} / 8 \mathrm{(bits/byte)} = 21333 \mathrm{(MB/s)}$. But there are times when PC4 is followed by MT/s.

Different generations of memory modules have different locations for the notches on the bottom pins, so it is impossible to insert them in the wrong place.

## Structure

Taking DDR4 SDRAM as an example, the following is the structure of the [MT40A1G8](https://www.micron.com/products/dram/ddr4-sdram/part-catalog/mt40a1g8sa-075) chip:

<figure markdown>
  ![](sdram_ddr4_micron_1g8_diagram.png){ width="800" }
  <figcaption>Block diagram of MT40A1G8 (Source <a href="https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/dram/ddr4/8gb_ddr4_sdram.pdf?rev=8634cc61670d40f69207f5f572a2bfdd">Micron Datasheet</a>)</figcaption>
</figure>

Each memory array is 65536 x 128 x 64, called a Bank; four Banks form a Bank Group, and there are 4 Bank Groups, so the total capacity is $65536 * 128 * 64 * 4 * 4 = 8 \mathrm{Gb}$.

Specifically, in the 65536 x 128 x 64 specification of each memory array, 65536 represents the number of rows, each row holds $128 * 64 = 8192$ bits of data, and is also the bit width of the transfer between `Sense amplifier` and `I/O gating, DM mask logic` in Figure 1. Each row has 1024 columns, and each column holds 8 bits of data (corresponding to the 8 in `1 Gig x 8`). Since the DDR4 prefetch width is 8n, an access takes out 8 columns of data, or 64 bits. So each row has 128 of 64 bits, which is the source of the 128 x 64 in the 65536 x 128 x 64 above.

## Prefetch

SDRAM has the concept of prefetch, which is how many times the bit width of the data is fetched out in one read. For example, the `1 Gig x 8` SDRAM above has an I/O data bit width of 8 bits (see the `DQ` signal on the right). This is because the IO frequency of DDR4 SDRAM is very high, e.g. 3200 MT/s corresponds to an I/O clock frequency of 1600 MHz, while the actual memory array frequency is not as high. The actual memory array frequency is that high, but operates at 400 MHz, so to make up for the difference in frequency, the data is read 8 times the bit width at a time. This is reflected in the I/O, which is a single read operation to get 8 copies of data, i.e. burst length of 8, which is transferred in four clock cycles via DDR.

Interestingly, DDR4 memory modules are 64 bits wide, so a single read operation yields $64 * 8 / 8 = 64B$ of data, which is exactly the size of the CPU cache lines.

DDR5 increases the prefetch to 16n, which is why you see much larger data rate numbers for DDR5: DDR4 prefetch is 8n, DDR5 prefetch is 16n at the same memory array frequency, so the I/O frequency is doubled and the data rate is doubled. At the same time, in order to maintain the burst size of 64 bytes, the bit width of each channel in DDR5 module is 32 bits, each memory module provides two channels.

## Access Patterns

SDRAM has a special access pattern in that its memory array can only be accessed in complete rows at a time. In the previous example, a row has 8192 bits of data, but a read or write operation involves only 64 bits of data, so a read operation requires:

1. the first step is to retrieve the entire row where the data is located
2. in the second step, read the desired data in the row

But each bank can only take out one row at a time, so if the two reads involve different rows, then you need to:

1. the first step is to take out the whole row where the data of the first read is located
2. in the second step, read the desired data in the row
3. step 3, put the first read row back
4. step 4, take out the whole row where the data of the second read is located
5. step 5, read the desired data in the row

In SDRAM terms, the first and fourth steps are called Activate, the second and fifth steps are called Read, and the third step is called Precharge.

SDRAM defines the following timing parameters that describe the timing requirements between these three operations:

1. CL (CAS Latency): the time between sending a read request and outputting the first data
2. RCD (ACT to internal read or write delay time): the time from Activate to the next read or write request
3. RP (RRE command period): the time between sending a Precharge command and the next command
4. RAS (ACT to PRE command period): the time between Activate and Precharge
5. RC (ACT to ACT or REF command period): the time between Activate and the next Activate or Refresh
6. RTP (Internal READ Command to PRECHARGE command delay): the time between Read and Precharge

So the above process requires the following time requirements:

1. the first step, Activate, take out the first row
2. the second step, Read, the time between the first and second steps should be separated by RCD, and the time to wait for CL from Read to send address to get data
3. step 3, Precharge, the time between step 1 and step 3 should be separated by RAS, and the time between step 2 and step 3 should be separated by RTP
4. step 4, Activate, take out the second row, the time between step 1 and step 4 should be separated by RC, and the time between step 3 and step 4 should be separated by RP
5. step 5, Read, the time between step 4 and step 5 should be separated by RCD, the time to wait for CL from Read to send address to get data

Based on this process, the following conclusions can be drawn:

1. accessing data with locality will have better performance, requiring only continuous Read, reducing the number of activates and precharges
2. constantly accessing data from different rows will lead to a back and forth Activate, Read, Precharge cycle
3. accessing the row and accessing the data in the row are divided into two phases, and both phases can use the same address signals, making the total memory capacity large
4. if the access always hits the same row, the transfer rate can be close to the theoretical one, as shown in Figure 2

<figure markdown>
  ![](sdram_ddr3_consecutive_read.png){ width="800" }
  <figcaption>DDR3 Sequential Reads within the Same Row (Source <a href="https://www.jedec.org/sites/default/files/docs/JESD79-3F.pdf">JESD9-3F DDR3</a>)</figcaption>
</figure>

To alleviate the performance loss caused by the second point, the concept of Bank is introduced: each Bank can take out a row, so if you want to access the data in different Banks, while the first Bank is doing Activate/Precharge, the other Banks can do other operations, thus covering the performance loss caused by row misses.

## Bank Group

DDR4 introduces the concept of Bank Group compared to DDR3. Quoting [Is the time of page hit in the same bank group tccd_S or tccd_L?](https://www.zhihu.com/question/59944554/answer/989376138), memory array frequency is increased compared to DDR3, so a perfect sequential read cannot be achieved within the same row, i.e. two adjacent read operations need to be separated by 5 cycles, while each read transfers 4 cycles of data with a maximum utilization of 80%, see the following figure:

<figure markdown>
  ![](sdram_ddr4_nonconsecutive_read.png){ width="800" }
  <figcaption>DDR4 Nonconsecutive Reads (Source <a href="https://www.jedec.org/document_search?search_api_views_fulltext=jesd79-4%20ddr4">JESD9-4D DDR4</a>)</figcaption>
</figure>

In order to solve this bottleneck, the difference of DDR4 in the core part is that there is an additional `Global I/O gating`, and each Bank Group has its own `I/O gating, DM mask logic`, the following draws the storage part of DDR3 and DDR4 respectively, for comparison:

<figure markdown>
  ![](sdram_ddr3_array.png){ width="400",align="left" }
  <figcaption>DDR3 SDRAM Storage Part (Source <a href="https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/dram/ddr3/1gb_ddr3_sdram.pdf?rev=22ebf6b7c48d45749034655015124500">Micron Datasheet</a>)</figcaption>
</figure>

<figure markdown>
  ![](sdram_ddr4_array.png){ width="400" }
  <figcaption>DDR4 SDRAM Storage Part (Source <a href="https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/dram/ddr4/8gb_ddr4_sdram.pdf?rev=8634cc61670d40f69207f5f572a2bfdd">Micron Datasheet</a>)</figcaption>
</figure>

This means that DDR4 can have multiple Bank Groups reading at the same time and pipelining the output. For example, if the first Bank Group reads the data and finishes transferring it in four cycles on the I/O, immediately the second Bank Group read picks up and transfers another four cycles of data, with the following waveform:

<figure markdown>
  ![](sdram_consecutive_read.png){ width="800" }
  <figcaption>DDR4 Consecutive Reads from Different Banks (Source <a href="https://www.jedec.org/document_search?search_api_views_fulltext=jesd79-4%20ddr4">JESD9-4D DDR4</a>)</figcaption>
</figure>

In the above figure, the first read request is initiated at time T0, the second request is initiated at time T4, T11-T15 get the data of the first request, followed by T15-T19 get the data of the second request. This solves the problem caused by the increased frequency.

## Storage Hierarchy

As mentioned above, the hierarchy within DDR SDRAM, from largest to smallest, is as follows

1. Bank Group: introduced in DDR4
2. Bank: Each Bank has only one Row activated at the same time
3. Row: Activate/Precharge unit
4. Column: each Column holds n cells, n is the bit width of SDRAM
5. Cell: each cell holds 1 bit of data

In fact, there are several layers outside the SDRAM:

1. Channel: the number of channels of the processor's memory controller
2. Module: there can be multiple memory sticks connected to the same Channel
3. Rank: multiple DDR SDRAM chips are stitched together in width, one to four Ranks can be put down on a Module. these Ranks share the bus, each Rank has its own chip select signal CS_n, which is actually stitching SDRAM chips in depth
4. Chip: A DDR SDRAM chip; such as a 64-bit wide Rank, is made by using 8 x8 chips stitched together across the width

As you can see, adjacent memory levels differ by a power of two, so the mapping from the memory address to these levels is an interception of different intervals in the address, each corresponding to a subscript of the level. This is why the MB and GB units of memory size are 1024-based.

If you study SDRAM memory controllers, such as [MIG on Xilinx FPGA](https://www.xilinx.com/support/documentation/ip_documentation/ultrascale_memory_ip/v1_4/pg150-ultrascale-memory-ip.pdf), one can find that it can be configured with different address mapping methods, e.g:

- ROW_COLUMN_BANK
- ROW_BANK_COLUMN
- BANK_ROW_COLUMN
- ROW_COLUMN_LRANK_BANK
- ROW_LRANK_COLUMN_BANK
- ROW_COLUMN_BANK_INTLV

As you can imagine, different address mapping methods will have different performance for different access modes. For sequential memory accesses, the ROW_COLUMN_BANK method is more suitable, because sequential accesses are distributed to different banks, so the performance will be better.

## Interface

The following pins are drawn for DDR3 and DDR4:

<figure markdown>
  ![](sdram_pinout.png){ width="600" }
  <figcaption>DDR3 and DDR4 Schematics</figcaption>
</figure>

The differences between DDR3 and DDR4:

1. address signal: DDR3 has A0-A14, DDR4 has A0-A17, where A14-A16 are multiplexed pins
2. DDR4 introduces Bank Group, so there are extra pins BA0-BA1.
3. RAS_n, CAS_n and WE_n in DDR3 are reused as A14-A16 in DDR4
4. DDR4 adds an additional ACT_n control signal

## Topology

In order to obtain a larger bit width, many SDRAM chips can be seen on the memory modules, which are stitched together by width to form a 64-bit data width. At this point, from the PCB alignment point of view, the data lines are directly connected to each SDRAM chip and can be connected relatively easily; however, other signals, such as address and control signals, need to be connected to all SDRAM chips, and it is difficult to ensure equal distances to each SDRAM chip while ensuring signal integrity in the confined space.

### Fly-by topology

Therefore, the address and control signals are actually connected in series (Fly-by-topology), which is the connection on the right in the following figure:

<figure markdown>
  ![](sdram_topology.png){ width="600" }
  <figcaption>Two types of signal connections for SDRAM (Source <a href="https://docs.xilinx.com/r/en-US/ug863-versal-pcb-design/Signals-and-Connections-for-DDR4-Interfaces">Versal ACAP PCB Design User Guide (UG863)</a>)</figcaption>
</figure>

But the data signals (DQ, DQS and DM) are still connected point-to-point to the SDRAM in parallel (left side of the figure above). This presents a problem: with different SDRAM chips, the data and clock deviations are different, and the data may arrive at about the same time, but the clock has an increasing delay:

<figure markdown>
```wavedrom
{
  signal:
    [
      { name: "clock", wave: "1010101010"},
      { name: "data", wave: "01.0..101."},
      { name: "clock_dram0", wave: "1010101010", phase: -0.2},
      { name: "data_dram0", wave: "01.0..101.", phase: -0.1},
      { name: "clock_dram1", wave: "1010101010", phase: -0.4},
      { name: "data_dram1", wave: "01.0..101.", phase: -0.1},
      { name: "clock_dram2", wave: "1010101010", phase: -0.6},
      { name: "data_dram2", wave: "01.0..101.", phase: -0.1},
      { name: "clock_dram3", wave: "1010101010", phase: -0.8},
      { name: "data_dram3", wave: "01.0..101.", phase: -0.1},
    ]
}
```
  <figcaption>SDRAM Clock Skewing Problem</figcaption>
</figure>

In order for SDRAMs at different locations to see the same waveform, a variable delay needs to be added to the data signal on the memory controller side, and this delay needs to be calibrated to know what it is.

### Clam-shell topology

In addition to Fly-by topology, Clam-shell topology may be used in some scenarios to save PCB area. Clam-shell is actually a visual representation of having SDRAM chips on both the front and back sides of the PCB:

<figure markdown>
  ![](sdram_clam_shell.png){ width="400" }
  <figcaption>Clam-shell Topology (Source <a href="https://docs.xilinx.com/r/en-US/pg313-network-on-chip/Clamshell-Topology">Versal ACAP Programmable Network on Chip and Integrated Memory Controller LogiCORE IP Product Guide (PG313) </a>)</figcaption>
</figure>

This design makes use of the space on the back of the PCB, but it also brings new problems: intuitively, if both chips are placed on the front of the PCB, it is easier to connect them if the pin order is close to the same, and there will not be many crossings. However, if one is on the front and the other on the back, the pin order is reversed and it is more difficult to connect.

The solution is to modify the order of the pins and swap the functions of some pins to make the alignment simpler:

<figure markdown>
  ![](sdram_pin_mirror.png){ width="600" }
  <figcaption>SDRAM Pin Mirroring (Source<a href="https://docs.xilinx.com/r/en-US/ug863-versal-pcb-design/Utilizing-Address-Mirroring-to-Ease-Clamshell-Routing">Versal ACAP PCB Design User Guide (UG863)</a>)</figcaption>
</figure>

The table deliberately selects pins to swap that do not affect special functions, making most functions, even with swapped pins, work properly. For example, if the Row address is swapped by a few bits, it does not affect reading or writing data, although the physical storage place is changed. However, for Mode Register Set operations, the memory controller must swap the order of the bits itself and swap them back when connecting on the PCB to ensure the correct result on the SDRAM side.

In addition, Clam-shell Topology has one cs_n chip select signal on the front and one on the back, but this is different from Dual Rank: Dual Rank has the same number of DRAM chips on both front and back, sharing the address, data and control signals, and only one side of the DRAM chips on the bus is in use at the same time, which has the advantage of doubling the memory capacity. The advantage is that the memory capacity is doubled and the two ranks can mask each other's latency; while the two cs_n of Clam Shell Topology are designed to assign either front or back side to Mode Register Set operations, while most of the rest of the operations can work on both front and back sides at the same time because their data signals are not shared.

## Calibration

SDRAM calibration, or SDRAM training, mainly consists of the following steps:

1. Write Leveling
2. Read Leveling

### Write Leveling

Write Leveling addresses the problem of inconsistent latency caused by Fly-by-Topology, which causes SDRAM to see the wrong signal. Specifically, the purpose of Write Leveling is to synchronize the DQS signal received by the SDRAM chip with the CK signal:

<figure markdown>
```wavedrom
{
  signal:
    [
      { name: "ck", wave: "1010101010"},
      { name: "dqs", wave: "0.101010.."},
      { name: "ck_dram0", wave: "1010101010", phase: -0.2},
      { name: "dqs_dram0", wave: "0.101010..", phase: -0.2},
      { name: "ck_dram1", wave: "1010101010", phase: -0.4},
      { name: "dqs_dram1", wave: "0.101010..", phase: -0.4},
      { name: "ck_dram2", wave: "1010101010", phase: -0.6},
      { name: "dqs_dram2", wave: "0.101010..", phase: -0.6},
      { name: "ck_dram3", wave: "1010101010", phase: -0.8},
      { name: "dqs_dram3", wave: "0.101010..", phase: -0.8},
    ]
}
```
  <figcaption>DQS and CK synchronization to be achieved by Write Leveling</figcaption>
</figure>

To achieve this, the idea is to continuously adjust the delay of the DQS output, observe the behavior at different delays, and find a delay value that synchronizes the DQS with the CK. In order to do Write Leveling with the memory controller, the SDRAM can enter a Write Leveling Mode, where the SDRAM samples the CK on the rising edge of the DQS and then outputs the result to the DQ. In this case, different DQS delays will result in different results:

<figure markdown>
```wavedrom
{
  signal:
    [
      { name: "ck", wave: "1010101010"},
      { name: "dqs", wave: "10........"},
      { name: "ck_dram", wave: "1010101010", phase: -0.2},
      { name: "dqs_delay0", wave: "010.......", phase: -0.4},
      { name: "dq_delay0", wave: "0.........", phase: -0.4},
      { name: "dqs_delay1", wave: "010.......", phase: -0.9},
      { name: "dq_delay1", wave: "0.........", phase: -0.9},
      { name: "dqs_delay2", wave: "010.......", phase: -1.4},
      { name: "dq_delay2", wave: "01........", phase: -1.4},
      { name: "dqs_delay3", wave: "010.......", phase: -2.0},
      { name: "dq_delay3", wave: "01........", phase: -2.0},
    ]
}
```
  <figcaption>Results of DQS sampling of CK with different DQS delays</figcaption>
</figure>

In the above figure, for both delay0 and delay1, DQS samples the negative half-cycle of CK, while for delay2 and delay3, DQS samples the positive half-cycle of CK, so if you want to synchronize DQS with CK, you should set the DQS delay between delay1 and delay2.

To summarize the Write Leveling algorithm:

1. Set the SDRAM to Write Leveling mode, where the SDRAM will use DQS for CK and output the result to DQ
2. The controller enumerates the latency of DQS, reads out the DQ results for each DQS latency, and gets a 0-1 string, for example: `00111111111111111111110000`, that is, as the latency increases, it samples to 0, then to 1, and finally to 0 again
3. find a DQS delay that causes the DQ to change from 0 to 1, then the DQS will be synchronized with the CK according to this delayed output
4. Set the SDRAM to end Write Leveling mode

This process is performed separately for each DQS signal. The following is an example of [litex's SDRAM calibration code](https://github.com/enjoy-digital/litex/blob/b367c27191511f36b10ec4103198978f86f9502c/litex/soc/software/liblitedram/sdram.c#L589) to implement a simplified process in C code:

```c title="int sdram_write_leveling_scan(int *delays, int loops, int show)" linenums="1"
/* Turn on the Write Leveling mode of SDRAM */
sdram_write_leveling_on();

/* Loop each SDRAM module */
for(i=0;i<SDRAM_PHY_MODULES;i++) {
  /* Loop each DQS signal */
  for (dq_line = 0; dq_line < DQ_COUNT; dq_line++) {
    /* Set initial DQS delay to 0 */
    sdram_leveling_action(i, dq_line, write_rst_delay);

    /* Loop each DQS delay */
    for(j=0;j<err_ddrphy_wdly;j++) {
      int zero_count = 0;
      int one_count = 0;

      /* Sample in loop */
      for (k=0; k<loops; k++) {
        /* Send DQS pulse：00000001 */
        /* SDRAM sample CK */
        ddrphy_wlevel_strobe_write(1);

        cdelay(100);
        /* Read DQ from memory controller */
        csr_rd_buf_uint8(sdram_dfii_pix_rddata_addr(0), buf, DFII_PIX_DATA_BYTES);

        /* Count the number of 1's and 0's */
        if (buf[SDRAM_PHY_MODULES-1-i] != 0)
          one_count++;
        else
          zero_count++;
      }
      if (one_count > zero_count)
        /* Consider that DQS samples the positive half-cycle of CK */
        taps_scan[j] = 1;
      else
        /* Consider that DQS samples the negative half-cycle of CK */
        taps_scan[j] = 0;

      /* Increases the DQS delay  */
      sdram_leveling_action(i, dq_line, write_inc_delay);
    }

    /* Find the longest sequence of consecutive 1's */
    one_window_active = 0;
    one_window_start = 0;
    one_window_count = 0;
    one_window_best_start = 0;
    one_window_best_count = -1;
    for(j=0;j<err_ddrphy_wdly+1;j++) {
      if (one_window_active) {
        if ((j == err_ddrphy_wdly) || (taps_scan[j] == 0)) {
          /* Ended a continuous sequence of 1's */
          one_window_active = 0;
          one_window_count = j - one_window_start;
          /* Record the length and position of the longest consecutive 1's */
          if (one_window_count > one_window_best_count) {
            one_window_best_start = one_window_start;
            one_window_best_count = one_window_count;
          }
        }
      } else {
        /* Find the beginning of consecutive 1's */
        if (j != err_ddrphy_wdly && taps_scan[j]) {
          one_window_active = 1;
          one_window_start = j;
        }
      }
    }

    /* The delay to be found is the start of a consecutive sequence of 1's */
    delays[i] = one_window_best_start;
  }
}

/* Turn off the Write Leveling mode of SDRAM */
sdram_write_leveling_off();
```

### Read Leveling

In the Write Leveling stage, the synchronization of signals at SDRAM is solved. However, for read operations, data is sent from SDRAM to the controller, and the time of arrival of different data to the controller may be different, so it is also necessary to calibrate the read operation.

To determine if the read data is correct, the practice is to first write known data and then read it out. If the read data is exactly the same as the written data, then the read operation can be performed correctly.

The implementation is similar to Write Leveling in that it enumerates the delays, performs some operations, and observes the output at each delay:

1. write data (or use SDRAM's function of generating a fixed pattern output)
2. set the latency to loop from 0
3. at each latency setting, read out the data and compare the read results with the previously written data
4. count which delay conditions, the read data is accurate. accurate is recorded as 1, inaccurate is recorded as 0
5. find the accurate range of 1, and take the midpoint as the final calibration result

Note that here is no longer to find the place of 0-1 change. Write Leveling to find 0-1 change is to synchronize, synchronization is exactly the place of 0-1 change; while the purpose of Read Leveling is to read out the correct data. It is known that there is a continuous delay interval, where it can read out the correct data. Even if the interval is shifted due to changes in temperature and other conditions, it will still work because enough margin is retained by taking the midpoint of the interval. The step of taking the midpoint is also called Read Centering.

## HBM

HBM is short for High Bandwidth Memory, and its technology is also based on SDRAM, so it is placed here for comparison with DDR SDRAM.

HBM stacks multiple SDRAMs, provides multiple channels and increases the bit width compared to the pDDR SDRAM. For example [Micron HBM with ECC](https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/dram/hbm2e/8gb_and_16gb_hbm2e_dram.pdf), stacks 4/8 layers of DRAM, provides 8 channels, each with a 128-bit data width. At 3200 MT/s, the maximum data transfer rate of an HBM chip is:

$$
3200 \mathrm{(MT/s)} * 128 \mathrm{(bits/transfer)} * 8 \mathrm{(Channels)} = 3276.8 \mathrm{(Gb/s)} = 409.6 \mathrm{(GB/s)}
$$

So a single HBM has the transfer rate of 16 traditional DDR SDRAMs, thanks to 8 channels and double the bit width. Each channel has a bit width of 128 bits, so it can be thought of as two 64-bit SDRAMs in parallel, either as one 128-bit SDRAM or, in Pseudo Channel mode, as two SDRAMs that share address and command signals.

Of course, the high bandwidth of HBM comes at the cost of a large number of pins. According to the [HBM3 JESD238A standard](https://www.jedec.org/system/files/docs/JESD238A.pdf), each channel requires 120 pins, for a total of 16 channels (HBM2 has 8 channels, 128 bits per channel; HBM3 has 16 channels, 64 bits per channel), plus the remaining 52 pins, which adds up to 1972 pins. So the connection to the processor is generally made on the Silicon Interposer, rather than the traditional PCB routing:

<figure markdown>
  ![](sdram_hbm_stack.png){ width="800" }
  <figcaption>HBM Packaging (Source <a href="https://picture.iczhiku.com/resource/ieee/WYifSuFTZuHLFcMV.pdf">A 1.2V 20nm 307GB/s HBM DRAM with At-Speed Wafer-Level I/O Test Scheme and Adaptive Refresh Considering Temperature Distribution</a>)</figcaption>
</figure>

So in the HBM3 standard, the pin is described as a microbump. HBM can be understood figuratively as taking the memory modules that were originally inserted into the motherboard and disassembling them, keeping only the chips, stacking them vertically and turning them into an HBM Die, which is then tightly connected to the CPU. But on the other hand, the density goes up, and the price gets more expensive. The scalability also went down, as you couldn't place as many HBM dies on the motherboard as you could with DDR SDRAM.

The following is an analysis of the memory bandwidth of some typical systems with HBM:

Xilinx's Virtex Ultrascale Plus HBM FPGA provides a bandwidth of $1800 \mathrm{(MT/s)} * 128 \mathrm{(bits/transfer)} * 8 \mathrm{(Channels)} = 230.4 \mathrm{(GB/s)}$. If two HBMs are used, that's 460.8 GB/s. Exposed to the FPGA logic are 16 256-bit AXI3 ports with an AXI frequency of 450 MHz and a memory frequency of 900 MHz. As you can see, each AXI3 corresponds to a pseudo channel of HBM. Each pseudo channel is 64 bits, but the AXI port is 256 bits. This is because going from 450MHz to 900MHz at the same rate, plus DDR, equates to a quadrupling of the frequency, so the bit width has to be quadrupled from 64 bits to 256 bits accordingly.

The 40GB PCIe version of the A100 graphics card uses five 8 GBs of HBM memory running at 1215 MHz, so the memory bandwidth is $1215 \mathrm{(MHz)} * 2 \mathrm{(DDR)} * 8 \mathrm{(channels)} * 128 \mathrm{(bits/ transfer)} / 8 \mathrm{(bits/byte)} * 5 \mathrm{(HBM)} = 1555 \mathrm{(GB/s)}$, which matches the Datasheet. The Memory bus width in the A100 Datasheet is actually calculated by adding up all the channel bit widths: $128 \mathrm{(bits/transfer)} * 8 \mathrm{(channels)} * 5 \mathrm{(stacks)} = 5120 \mathrm{(bits)}$.

The 80GB PCIe version of the A100 graphics card upgrades HBM2 to HBM2e, and the memory clock frequency is upgraded to 1512 MHz, so the memory bandwidth is $1512 \mathrm{(MHz)} * 2 \mathrm{(DDR)} * 8 \mathrm{(channels)} * 128 \mathrm{( bits/transfer)} / 8 \mathrm{(bits/byte)} * 5 \mathrm{(HBM)} = 1935 \mathrm{(GB/s)}$, which coincides with Datasheet.

The 80GB SXM5 version of the H100 graphics card upgrades HBM to HBM3, and the memory capacity remains the same at 80GB, but the clock frequency is increased to 2619 MHz, at which point the memory bandwidth is $2619 \mathrm{(MHz)} * 2 \mathrm{(DDR)} * 8 \mathrm{(channels)} * 128 \ mathrm{(bits/transfer)} / 8 \mathrm{(bits/byte)} * 5 \mathrm{(HBM)} = 3352 \mathrm{(GB/s)}$.

## DRAM Cell

Data in DRAM is stored in capacitors. The internal structure of a typical 1T DRAM Cell is as follows:

<figure markdown>
  ![1T DRAM Cell](sdram_dram_cell.png){ width="400" }
  <figcaption>1T DRAM Cell Internal Structure (Source <a href="https://inst.eecs.berkeley.edu/~eecs151/sp19/files/lec16-ram.pdf">Berkeley EECS 151/251A Spring 2019</a>)</figcaption>
</figure>

## Comparison of DDR variants

A comparison of DDR, LPDDR, GDDR and HBM is given below:

|              | DDR4      | DDR5      | LPDDR4    | LPDDR5    | GDDR5   | GDDR6   | HBM2     |
| ------------ | --------- | --------- | --------- | --------- | ------- | ------- | -------- |
| Channels   | 1         | 2         | 2         | 2         | 2       | 2       | 8        |
| Bits per Channel | 64        | 32        | 16        | 16/32     | 16      | 16      | 128      |
| Data rate (MT/s)   | 3200      | 5600      | 4266      | 6400      | 9000    | 24000   | 2400     |
| Bandwidth (GB/s)  | 25.6 GB/s | 44.8 GB/s | 17.1 GB/s | 25.6 GB/s | 36 GB/s | 96 GB/s | 307 GB/s |

Data rates are based on the highest performance available:

- DDR4: [Micron 3200 MT/s](https://www.micron.com/-/media/client/global/documents/products/data-sheet/dram/ddr4/8gb_ddr4_sdram.pdf)
- DDR5: [Micron 5600 MT/s](https://media-www.micron.com/-/media/client/global/documents/products/part-numbering-guide/micron_ddr5_part_catalog.pdf?la=en&rev=a4865faa98834095b94db57e7bd394e1)
- LPDDR4: [Samsung 4266 MT/s](https://semiconductor.samsung.com/dram/lpddr/lpddr4/)
- LPDDR5: [Samsung 6400 MT/s](https://semiconductor.samsung.com/dram/lpddr/lpddr5/)
- GDDR5: [Samsung 9000 MT/s](https://semiconductor.samsung.com/dram/gddr/gddr5/)
- GDDR6: [Samsung 24000 MT/s](https://semiconductor.samsung.com/dram/gddr/gddr6/)
- HBM2: [Samsung 2400 MT/s](https://semiconductor.samsung.com/dram/hbm/hbm2-aquabolt/)
- HBM2E: [Micron 3200 MT/s](https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/dram/hbm2e/8gb_and_16gb_hbm2e_dram.pdf)


## Related Reading

- [DDR4 Bank Groups in Embedded Applications](https://www.synopsys.com/designware-ip/technical-bulletin/ddr4-bank-groups.html)
- [DDR4 Tutorial - Understanding the Basics](https://www.systemverilog.io/design/ddr4-basics/)
- [DDR5/4/3/2: How Memory Density and Speed Increased with each Generation of DDR](https://blogs.synopsys.com/vip-central/2019/02/27/ddr5-4-3-2-how-memory-density-and-speed-increased-with-each-generation-of-ddr/)
- [DDR5 vs DDR4 DRAM – All the Advantages & Design Challenges](https://www.rambus.com/blogs/get-ready-for-ddr5-dimm-chipsets/)
- [Understanding DDR3 Write Leveling and Read Leveling](https://daffy1108.wordpress.com/2010/09/02/understanding-ddr3-write-leveling-and-read-leveling/)
- [Will HBM replace DDR and become Computer Memory?](https://www.utmel.com/blog/categories/memory%20chip/will-hbm-replace-ddr-and-become-computer-memory)

## Acknowledgement

The English version is kindly translated with the help of DeepL Translator.
