# Examples

Examples of using `noc` to interact with [Netflix Open Content](https://opencontent.netflix.com/) media.

- [Examples](#examples)
  - [Browse](#browse)
  - [List](#list)
  - [Download](#download)
    - [Resume or Extend Download](#resume-or-extend-download)
    - [Download and Rename](#download-and-rename)
    - [Download, Rename, and Renumber](#download-rename-and-renumber)

## Browse

Open a web browser to the Netflix Open Content URL.

```bash
noc browse
```

## List

List content with frames (default).

```bash
noc list
```

Output:

```bash
Available content with frames:
- chimera             : Live action footage, 4K. Download configured for the 23.98fps frame rate version. TIFF files.
- cosmoslaundromat    : Animated short film done in Blender, 2K 24p. EXR files.
- meridian            : Live action noir UHD short, 59.94fps. Mastered in Dolby Vision HDR. TIFF files.
- sparks              : Live action 4K HDR test short, 59.94fps, finished at 4000 nits. ACES EXR files.
```

List all content (some content does not have frames for download).

```bash
noc list --no-only-frames
```

Output:

```bash
Available content:
- chimera             : Live action footage, 4K. Download configured for the 23.98fps frame rate version. TIFF files.
- cosmoslaundromat    : Animated short film done in Blender, 2K 24p. EXR files.
- elfuente            : 4K live action footage.
- meridian            : Live action noir UHD short, 59.94fps. Mastered in Dolby Vision HDR. TIFF files.
- nocturne            : Live action test piece at 120fps. Mastered in Dolby Vision HDR and Dolby Atmos.
- sollevante          : 4K HDR Atmos anime short.
- sparks              : Live action 4K HDR test short, 59.94fps, finished at 4000 nits. ACES EXR files.
```

## Download

Download frames 1-5 from [Sparks](https://opencontent.netflix.com/#h.d0oh6u8prqhe)

```bash
noc download sparks -fs 1 -fe 5
```

Output:

```bash
Downloading: sparks frames 1-5
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:57
```

### Resume or Extend Download

Download frames 1-8 from [Sparks](https://opencontent.netflix.com/#h.d0oh6u8prqhe)

```bash
noc download sparks -fs 4 -fe 8
```

Frames that already exist on disk are skipped by default. Use `--force` to force re-download and overwrite.

Output:

```bash
Downloading: sparks frames 4-8
file SPARKS_ACES_00004.exr exists, skipping. Use --force to overwrite.
file SPARKS_ACES_00005.exr exists, skipping. Use --force to overwrite.
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:34
```

### Download and Rename

Download frames 21000-21005 from [Meridian](https://opencontent.netflix.com/#h.fzfk5hndrb9w) and rename as 'meridian.%05d.tif'

```bash
noc download meridian -fs 21000 -fe 21005 --rename meridian.%05d.tif
```

Output:

```bash
noc download meridian -fs 21000 -fe 21005 --rename meridian.%05d.tif
Downloading: meridian frames 21000-21005
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:01:12
```

### Download, Rename, and Renumber

Download frames 9911-9963 of [Cosmos Laundromat](https://opencontent.netflix.com/#h.uyzoa2bivz2j), renaming as COS_002_0045_comp_NFX_v001.%04d.exr, and renumbering to start at frame 1001 rather than 9911.

```bash
noc download cosmoslaundromat -fs 9911 -fe 9963 --rename COS_002_0045_comp_NFX_v001.%04d.exr --renumber 1001
```

Output:

```bash
Downloading: cosmoslaundromat frames 9911-9963
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:07:03
```

This example uses [Netflix VFX Shot and Version Naming Recommendations](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360057627473-VFX-Shot-and-Version-Naming-Recommendations) to compose the new name.

The example also makes the assumptions that [Cosmos Laundromat](https://opencontent.netflix.com/#h.uyzoa2bivz2j):

- is a feature, not an episodic
- uses scenes, but not sequences
- the frames represent iteration v001 of VFX comp (composite) work by NFX (Netflix), the vendor.

Shot Fields:

- showID (COS)
- episode (n/a)
- seq (not used)
- scene (002)
- shotID# (0045)

Version Fields:

- task (comp)
- vendorID (NFX)
- version# (v001)
