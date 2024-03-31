# coding=utf-8
#
# Copyright 2024 Toshihiko Aoki
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to ion writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import langid
import pysbd
import ctranslate2
import transformers
import unicodedata


class Translate:

    def __init__(
        self,
        model_path="../ct2-madlad400-3b-mt-int8",
        tokenizer_path="jbochi/madlad400-3b-mt", device='cpu',
        convert_target='ja',
    ):
        self.translator = ctranslate2.Translator(model_path, device)
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(tokenizer_path)
        self.convert_rule = '<2' + convert_target + '>'

    def _translate(self, text):
        # https://forum.opennmt.net/t/ctranslate2-supports-madlad-400/5564/2
        input_text = self.convert_rule + text
        input_tokens = self.tokenizer.convert_ids_to_tokens(
            self.tokenizer.encode(input_text, max_length=510, truncation=True))
        results = self.translator.translate_batch([input_tokens])
        output_tokens = results[0].hypotheses[0]
        return self.tokenizer.decode(self.tokenizer.convert_tokens_to_ids(output_tokens))

    def translate(self, text):
        lang, score = langid.classify(text)
        if lang in self.convert_rule:
            return text
        result = ""

        if pysbd.languages.LANGUAGE_CODES.get(lang) is not None:
            segmenter = pysbd.Segmenter(language=lang, clean=False)
            for seg in segmenter.segment(text):
                result += self._translate(seg)
        else:
            result = self._translate(text)

        return unicodedata.normalize('NFKC', result)
