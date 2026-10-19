"""Video processing as parallel work: split a video into segments, transcode each segment into several renditions on many
workers, then package. Run: python3 video_dag.py"""
import math


def makespan(segments, renditions, workers, seconds_per_job):
    jobs = segments * renditions
    return math.ceil(jobs / workers) * seconds_per_job


if __name__ == "__main__":
    # a 10-minute video, 10-second segments, 5 renditions, 4 seconds to transcode one segment-rendition, 30 workers
    segs, rends, per_job = 60, 5, 4
    serial = makespan(segs, rends, 1, per_job)
    one_per_video = makespan(1, rends, rends, per_job * segs)       # one worker per rendition, whole video each
    parallel = makespan(segs, rends, 30, per_job)
    print(f"{segs * rends} segment-rendition jobs: one worker {serial} s, one worker per rendition {one_per_video} s, 30 workers on segments {parallel} s")
    assert serial == 1200 and one_per_video == 240 and parallel == 40
    print("video dag ok")
