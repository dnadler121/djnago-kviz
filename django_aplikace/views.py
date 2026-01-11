from django.shortcuts import render, redirect
from .models import VysledekKvizu
from django.views.decorators.http import require_POST
from django.conf import settings


OTAZKY = [
    {"id": 1, "text": "Které zvíře je nejrychlejší na zemi?",
     "moznosti": {"A": "Gepard", "B": "Lev", "C": "Slon"}, "spravna": "A"},

    {"id": 2, "text": "Které zvíře je největší suchozemský savec?",
     "moznosti": {"A": "Nosorožec", "B": "Slon africký", "C": "Hroch"}, "spravna": "B"},

    {"id": 3, "text": "Jak se jmenuje mládě ovce?",
     "moznosti": {"A": "Jehně", "B": "Tele", "C": "Kůzle"}, "spravna": "A"},

    {"id": 4, "text": "Který pták nelétá?",
     "moznosti": {"A": "Orel", "B": "Tučňák", "C": "Vlaštovka"}, "spravna": "B"},

    {"id": 5, "text": "Který živočich dýchá žábrami po celý život?",
     "moznosti": {"A": "Kapr", "B": "Žába", "C": "Ještěrka"}, "spravna": "A"},

    {"id": 6, "text": "Které zvíře dokáže měnit barvu kůže?",
     "moznosti": {"A": "Chameleon", "B": "Vlk", "C": "Srna"}, "spravna": "A"},

    {"id": 7, "text": "Které zvíře používá echolokaci?",
     "moznosti": {"A": "Netopýr", "B": "Ježek", "C": "Veverka"}, "spravna": "A"},

    {"id": 8, "text": "Které zvíře je největší na světě?",
     "moznosti": {"A": "Žralok bílý", "B": "Plejtvák obrovský", "C": "Slon"}, "spravna": "B"},

    {"id": 9, "text": "Které zvíře patří mezi vačnatce?",
     "moznosti": {"A": "Klokan", "B": "Panda", "C": "Polární liška"}, "spravna": "A"},

    {"id": 10, "text": "Která kočkovitá šelma je největší?",
     "moznosti": {"A": "Gepard", "B": "Tygr", "C": "Rys"}, "spravna": "B"},

    {"id": 11, "text": "Které zvíře je symbolem Austrálie?",
     "moznosti": {"A": "Klokan", "B": "Pštros", "C": "Medvěd"}, "spravna": "A"},

    {"id": 12, "text": "Které zvíře má nejdelší krk?",
     "moznosti": {"A": "Kůň", "B": "Žirafa", "C": "Velbloud"}, "spravna": "B"},

    {"id": 13, "text": "Které zvíře spí přes zimu zimním spánkem?",
     "moznosti": {"A": "Medvěd", "B": "Liška", "C": "Jelen"}, "spravna": "A"},

    {"id": 14, "text": "Které zvíře je považováno za krále zvířat?",
     "moznosti": {"A": "Tygr", "B": "Lev", "C": "Gepard"}, "spravna": "B"},

    {"id": 15, "text": "Které zvíře má bodliny?",
     "moznosti": {"A": "Ježek", "B": "Králík", "C": "Pes"}, "spravna": "A"},

    {"id": 16, "text": "Které zvíře je největší pták na světě?",
     "moznosti": {"A": "Orel", "B": "Pštros", "C": "Kondor"}, "spravna": "B"},

    {"id": 17, "text": "Které zvíře žije převážně ve vodě?",
     "moznosti": {"A": "Delfín", "B": "Pes", "C": "Kůň"}, "spravna": "A"},

    {"id": 18, "text": "Které zvíře má chobot?",
     "moznosti": {"A": "Nosorožec", "B": "Slon", "C": "Hroch"}, "spravna": "B"},

    {"id": 19, "text": "Které zvíře klade vejce?",
     "moznosti": {"A": "Kachna", "B": "Pes", "C": "Kočka"}, "spravna": "A"},

    {"id": 20, "text": "Které zvíře je známé svou pomalostí?",
     "moznosti": {"A": "Lenochod", "B": "Gepard", "C": "Kůň"}, "spravna": "A"},
]


def prihlaseni(request):
    chyba = None

    if request.method == "POST":
        jmeno = request.POST.get("jmeno", "").strip()

        if not jmeno:
            chyba = "Zadej prosím jméno."
        else:
            request.session["jmeno"] = jmeno
            return redirect("kviz")

    return render(request, "prihlaseni.html", {"chyba": chyba})



def kviz(request):
    jmeno = request.session.get("jmeno")

    if not jmeno:
        return redirect("prihlaseni")

    if request.method == "POST":
        skore = 0
        radky = []

        for o in OTAZKY:
            vybrano = request.POST.get(f"q{o['id']}")
            if vybrano == o["spravna"]:
                skore += 1

            radky.append(f"{o['id']}) vybráno: {vybrano}, správně: {o['spravna']}")

        # uložíme do DB a vezmeme si vytvořený objekt
        vysledek = VysledekKvizu.objects.create(
            jmeno=jmeno,
            skore=skore,
            max_skore=len(OTAZKY),
            detail="\n".join(radky),
        )

        # aby žák viděl výsledek – uložíme id do session
        request.session["posledni_vysledek_id"] = vysledek.id

        # žáka "odhlásíme" z kvízu (aby nešel refreshovat/odesílat znovu)
        request.session.pop("jmeno", None)

        return redirect("hotovo")

    return render(request, "kviz.html", {"otazky": OTAZKY, "jmeno": jmeno})


def hotovo(request):
    # stránka výsledku pro žáka
    vid = request.session.get("posledni_vysledek_id")
    if not vid:
        return render(request, "hotovo.html", {"vysledek": None})

    vysledek = VysledekKvizu.objects.filter(id=vid).first()
    return render(request, "hotovo.html", {"vysledek": vysledek})



def _ucitel_ok(request) -> bool:
    return bool(request.session.get("ucitel_ok"))


def ucitel_prihlaseni(request):
    chyba = None
    if request.method == "POST":
        heslo = request.POST.get("heslo", "")
        if heslo == getattr(settings, "UCITEL_HESLO", ""):
            request.session["ucitel_ok"] = True
            return redirect("ucitel")
        chyba = "Nesprávné heslo."

    return render(request, "ucitel_prihlaseni.html", {"chyba": chyba})


def ucitel_odhlasit(request):
    request.session.pop("ucitel_ok", None)
    return redirect("ucitel_prihlaseni")


def ucitel(request):
    if not _ucitel_ok(request):
        return redirect("ucitel_prihlaseni")

    zaznamy = VysledekKvizu.objects.order_by("-created_at")
    return render(request, "ucitel.html", {"zaznamy": zaznamy})


@require_POST
def vymazat_vysledky(request):
    if not _ucitel_ok(request):
        return redirect("ucitel_prihlaseni")

    VysledekKvizu.objects.all().delete()
    return redirect("ucitel")





