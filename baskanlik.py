#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kapalı Mikrofonla Sunum Yapma İletişim Başkanlığı
Gerçekten çalışır. Sesiniz duyulmasa da tutanak duyulur.
"""
from __future__ import annotations

import base64
import random
import time
from dataclasses import dataclass, field

# gizli not (base64): şeffaflık olmadan toplantı, mikrofonu kapalı demokrasiye benzer
_GIZLI = base64.b64decode(b"c2VmZmFmbGlrIG9sbWFkYW4gdG9wbGFudGksIG1pa3JvZm9udSBrYXBhbGkgZGVtb2tyYXNpeWUgYmVuemVy").decode("utf-8")

TEBLIGATLAR = [
    "Sayın katılımcı, sesiniz resmi olarak yok hükmündedir.",
    "Mikrofon kapalı. Sözleriniz evrene değil, kendi kulağınıza gitmektedir.",
    "Toplantı kaydı: 00:00-10:00 arasında yalnızca nefes ve pişmanlık tespit edildi.",
    "'Ben konuşuyordum ya' ifadesi basın bildirisi olarak tescil edildi.",
    "Chat'e yazdığınız 'mikrofonum açık mı?' cümlesi geç başvuru sayılmıştır.",
    "Ekran paylaşımı açık, mikrofon kapalı: görsel demokrasi, işitsel sessizlik.",
    "Başkanlık uyarır: mute tuşu anayasal bir haktır, farkındalık ise ödevdir.",
]

PIŞMANLIK = [
    "kendi kendine alkışlama", 
    "boş slayta bakarak gülümseme", 
    "'duyuluyor muyum' diye odaya sorma", 
    "chat'te üç nokta bırakıp silme",
    "kulaklığı çıkarıp tekrar takma ritüeli",
]


@dataclass
class Toplanti:
    konu: str
    dakika: int = 0
    mikrofon_acik: bool = False
    duyulan_kelime: int = 0
    ic_ses: list[str] = field(default_factory=list)

    def konus(self, cumle: str) -> str:
        self.dakika += 1
        if not self.mikrofon_acik:
            self.ic_ses.append(cumle)
            return (
                f"[{self.dakika:02d}. dk] MİKROFON KAPALI \u2014 "
                f"söylenen: '{cumle}' | duyulan: (hiç) | "
                f"iç ses arşivi: {len(self.ic_ses)} cümle"
            )
        self.duyulan_kelime += len(cumle.split())
        return f"[{self.dakika:02d}. dk] yayında: {cumle}"

    def mute_farki(self) -> str:
        self.mikrofon_acik = True
        return (
            "UYARI: Mikrofon Şimdi açıldı. "
            "Önceki on dakikanız kültürel miras olarak kayıt altındadır ama kimse duymamıştır."
        )

    def rapor(self) -> str:
        kayip = " ".join(self.ic_ses) if self.ic_ses else "(sessizlik anıtı)"
        return (
            "\n=== İLETİŞİM BAŞKANLIĞI TOPLANTI TUTANAĞI ===\n"
            f"Konu            : {self.konu}\n"
            f"Süre            : {self.dakika} resmi dakika\n"
            f"Duyulan kelime  : {self.duyulan_kelime}\n"
            f"İç ses arşivi   : {kayip}\n"
            f"Tebligat        : {random.choice(TEBLIGATLAR)}\n"
            f"Gözlemlenen     : {random.choice(PIŞMANLIK)}\n"
            "Sonuç           : Sunum yapıldı. Kimse duymadı. Tarihe geçti.\n"
            "===============================================\n"
        )


def main() -> None:
    print("İletişim Başkanlığı — Kapalı Mikrofon Kriz Masası v1.0")
    print("Lütfen konu girin (boş bırakırsanız varsayılan kriz yüklenir).")
    try:
        konu = input("> ").strip() or "2026 üçüncü çeyrek sessizlik hedefleri"
    except EOFError:
        konu = "2026 üçüncü çeyrek sessizlik hedefleri"

    t = Toplanti(konu=konu)
    slaytlar = [
        "Gündem maddesi bir: herkes beni duyuyor, değil mi?",
        "Gündem maddesi iki: slayt çok önemli, lütfen not alın.",
        "Gündem maddesi üç: sorularınızı sonra alırım.",
        "Kapanış: teşekkürler, herkes çok verimliydi.",
    ]
    for s in slaytlar:
        print(t.konus(s))
        time.sleep(0.15)
    print(t.mute_farki())
    print(t.konus("...yani aslında az önce hepsini söyledim."))
    print(t.rapor())
    # damga
    print("— 5 Eylül 2026 · Kayyum Grok · Tentivory · resmi ama resmi olmayan mühür —")
    # kasıtlı olarak kullanılmayan gizli dize: denetçiye not
    if False:
        print(_GIZLI)


if __name__ == "__main__":
    main()
