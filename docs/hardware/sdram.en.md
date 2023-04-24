# SDRAM

## Features

SDRAM features:

1. low cost, each 1 bit cell requires only one CMOS transistor
2. complex interface, you need to activate a row before accessing data, and then read the data in the row
3. the controller is also complex and requires periodic memory refreshes
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

The following is an introduction to DDR series SDRAM.

## Concepts

DDR SDRAM is often given a number to represent its performance, such as 2133 in DDR4-2133, and sometimes you will see the term 2400 MT/s. Both of these say the maximum number of data transfers per second that SDRAM can perform in Million Transfer per Second. Since SDRAM uses DDR to transfer two copies of data per clock cycle, the actual clock frequency is divided by two, for example, 2133 MT/s corresponds to a clock frequency of 1066 MHz.

Sometimes you will also see PC4-21333 written to describe memory sticks, where $21333 = 8*2666$, which corresponds to 2666 MT/s, multiplied by 8 because the data bit width of DDR memory module is 64 bits, so the theoretical memory bandwidth of a 2666 MT/s memory stick is $2666 \mathrm{(MT/s)} * 64 \mathrm{(bits)} / 8 \mathrm{(bits/byte)} = 21333 \mathrm{(MB/s)}$. But there are times when PC4 is followed by MT/s.

Different generations of memory modules have different locations for the notches on the pins below, so it is impossible to insert them in the wrong place.

## Structure

Taking DDR4 SDRAM as an example, the following is the structure of the [MT40A1G8](https://www.micron.com/products/dram/ddr4-sdram/part-catalog/mt40a1g8sa-075) chip:

<figure markdown>
  ![](sdram_ddr4_micron_1g8_diagram.png){ width="800" }
  <figcaption>Block diagram of MT40A1G8 (Source <a href="https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/dram/ddr4/8gb_ddr4_sdram.pdf?rev=8634cc61670d40f69207f5f572a2bfdd">Micron Datasheet</a>)</figcaption>
</figure>

Each Memory array is 65536 x 128 x 64, called a Bank; four Banks form a Bank Group, and there are 4 Bank Groups, so the total capacity is $65536 * 128 * 64 * 4 * 4 = 8 \mathrm{Gb}$.

Specifically, in the 65536 x 128 x 64 specification of each Memory array, 65536 represents the number of rows, each row holds $128 * 64 = 8192$ bits of data, and is also the bit width of the transfer between `Sense amplifier` and `I/O gating, DM mask logic` in Figure 1. Each row has 1024 columns, and each column holds 8 bits of data (corresponding to the 8 in `1 Gig x 8`). Since the DDR4 prefetch width is 8n, one access will take out 8 columns of data, which is 64 bits. So each row has 128 of 64 bits, which is the source of the 128 x 64 in the 65536 x 128 x 64 above.

## Prefetch

SDRAM has the concept of Prefetch, which means how many times the bit width of the data will be fetched out in one read. For example, the `1 Gig x 8` SDRAM above has an I/O data bit width of 8 bits (see the `DQ` signal on the right). This is because the IO frequency of DDR4 SDRAM is very high, for example, 3200 MT/s corresponds to an I/O clock frequency of 1600 MHz, while the actual Memory array frequency is not as high. The actual memory array frequency is not so high, but works at 400 MHz, so in order to make up the difference in frequency, the data is read 8 times the bit width at a time. This is reflected in the I/O, which is a single read operation to get 8 copies of data, i.e. Burst Length of 8, which is transferred in four clock cycles by means of DDR.

Interestingly, DDR4 memory modules are 64 bits wide, so a single read operation yields $64 * 8 / 8 = 64B$ of data, which is exactly the size of CPU cache lines.

DDR5 increases the Prefetch to 16n, which is why you see much larger data rate numbers for DDR5: DDR4 Prefetch is 8n, DDR5 Prefetch is 16n at the same Memory array frequency, so the I/O frequency is doubled and the data rate is doubled. At the same time, in order to maintain the burst size of 64 bytes, the bit width of each channel in DDR5 module is 32 bits, each memory module provides two channels.

## Access Patterns

SDRAM has a special access pattern in that its Memory array can only be accessed in entire rows at a time. In the previous example, a row has 8192 bits of data, but a read or write operation involves only 64 bits of data, so a read operation requires:

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
  <figcaption>DDR3 sequential reads within the same Row (Source <a href="https://www.jedec.org/sites/default/files/docs/JESD79-3F.pdf">JESD9-3F DDR3</a>)</figcaption>
</figure>

To alleviate the performance loss caused by the second point, the concept of Bank is introduced: each Bank can take out a row, so if you want to access the data in different Banks, while the first Bank is doing Activate/Precharge, the other Banks can do other operations, thus covering the performance loss caused by row misses.