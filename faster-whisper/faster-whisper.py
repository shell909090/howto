#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2023-03-26
@author: Shell.Xu
@copyright: 2023, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import os
import sys
import time
import logging
import argparse
import datetime
from os import path

from faster_whisper import WhisperModel


logger = logging.getLogger()
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


FILE_EXTS = {'.mp3', '.aac'}


def txt_writer(fn, segments):
    basefn = path.splitext(fn)[0]
    with open(f'{basefn}.txt', 'w') as fo:
        for segment in segments:
            fo.write(f'{segment.text}\n')


def fmt_time(t):
    s = int(t) % 60
    m = int(int(t) / 60)
    return f'{int(m / 60):02}:{m % 60:02}:{s:02},{int(t*1000) % 1000:03}'


def srt_writer(fn, segments):
    basefn = path.splitext(fn)[0]
    with open(f'{basefn}.srt', 'w') as fo:
        for i, segment in enumerate(segments):
            fo.write(f'{i+1}\n{fmt_time(segment.start)} --> {fmt_time(segment.end)}\n{segment.text}\n\n')


def proc_file(fn):
    basefn = path.splitext(fn)[0]
    if path.exists(f'{basefn}.txt'):
        logging.info(f'{fn} has been processed before.')
        return

    logging.info(f'Processing {fn}...')
    st = time.time()

    try:
        segments, info = model.transcribe(fn, beam_size=5)
        logging.info("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        cached = []
        for segment in segments:
            logging.info(f'[{segment.start:.2f} -> {segment.end:.2f}] {segment.text}')
            cached.append(segment)

        txt_writer(fn, cached)
        srt_writer(fn, cached)

    except Exception:
        logging.exception(f'Failed to processing {fn}.')

    logging.info(f'{fn} done in {time.time()-st}s.')


def recursion(fn):
    for root, dirs, files in os.walk(fn):
        for f in files:
            if path.splitext(f)[1].lower() in FILE_EXTS:
                yield path.join(root, f)


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='large-v2')
    parser.add_argument('--device', '-d', default='cpu')
    parser.add_argument('--compute-type', '-ct', default='int8')
    parser.add_argument('--recursion', '-R', action='store_true')
    parser.add_argument('files', nargs='*', type=str)
    args = parser.parse_args()

    global model
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)

    for fn in args.files:
        if args.recursion:
            for fp in recursion(fn):
                proc_file(fp)
        else:
            proc_file(fn)


if __name__ == '__main__':
    main()
