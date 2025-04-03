#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2025-04-03
@author: Shell.Xu
@copyright: 2025, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import re
import time
import logging
import argparse
from os import path

from funasr import AutoModel

model_dir = "iic/SenseVoiceSmall"


tag = re.compile(r'<\|\w+\|><\|\w+\|><\|\w+\|><\|\w+\|>')
def transcription(fp):
    res = model.generate(
        input=fp,
        cache={},
        language=args.language,
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15)
    return tag.sub('\n', res[0]['text'])


def proc_file(fp):
    basefp = path.splitext(fp)[0]
    if path.exists(f'{basefp}.txt'):
        logging.info(f'{fp} has been processed before.')
        return

    logging.info(f'Processing {fp}...')
    st = time.time()

    try:
        content = transcription(fp)
        with open(f'{basefp}.txt', 'w') as fo:
            fo.write(content)

    except Exception:
        logging.exception(f'Failed to processing {fp}.')

    logging.info(f'{fp} done in {time.time()-st}s.')


def recursion(fn):
    for root, dirs, files in os.walk(fn):
        for f in files:
            if path.splitext(f)[1].lower() in FILE_EXTS:
                yield path.join(root, f)


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', '-lg', default='auto', help='language')
    parser.add_argument('--device', '-d', default='cpu')
    parser.add_argument('--recursion', '-R', action='store_true')
    parser.add_argument('rest', nargs='*', type=str)
    args = parser.parse_args()

    global model
    model = AutoModel(
        model=model_dir,
        trust_remote_code=True,
        remote_code="./model.py",  
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device=args.device)

    for fn in args.rest:
        if args.recursion:
            for fp in recursion(fn):
                proc_file(fp)
        else:
            proc_file(fn)


if __name__ == '__main__':
    main()
