import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import engine

MAX_INPUT_CHARS = 20_000


def _run(text):
    tokens = engine.parse_mutations(text[:MAX_INPUT_CHARS])
    known, unknown = engine.resolve(tokens)
    return known, unknown, engine.predict(known)


def index(request):
    model = engine.load_model()
    text = request.GET.get("mutations", "")
    context = {
        "text": text,
        "examples": [{**e, "query": ", ".join(e["mutations"])} for e in engine.EXAMPLES],
        "features": model["features"],
        "n_features": len(model["features"]),
        "n_isolates": model["n_isolates"],
    }
    if "mutations" in request.GET:
        known, unknown, results = _run(text)
        for r in results:
            r["pct"] = round(r["probability"] * 100)
        reliable = [r for r in results if r["reliable"]]
        context.update(known=known, unknown=unknown, results=results, n_reliable=len(reliable),
                       n_resistant=sum(r["call"] == "R" for r in reliable))
    return render(request, "predictor/index.html", context)


def model_card(request):
    model = engine.load_model()
    return render(request, "predictor/model.html", {
        "rows": engine.metrics_table(),
        "model": model,
        "n_features": len(model["features"]),
        "reliable_auc": engine.RELIABLE_AUC,
        "reliable_lab": engine.RELIABLE_UNSEEN_LAB,
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_predict(request):
    """GET /api/predict?mutations=katG_S315T,rpoB_S450L
    POST /api/predict  {"mutations": ["katG_S315T", "rpoB_S450L"]}"""
    if request.method == "POST":
        try:
            body = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Body must be JSON, e.g. {\"mutations\": [\"katG_S315T\"]}"}, status=400)
        muts = body.get("mutations", [])
        if not isinstance(muts, list) or not all(isinstance(m, str) for m in muts):
            return JsonResponse({"error": "\"mutations\" must be a list of strings"}, status=400)
        text = ", ".join(muts)
    else:
        text = request.GET.get("mutations", "")
    known, unknown, results = _run(text)
    return JsonResponse({
        "recognised": known,
        "not_in_model": unknown,
        "threshold": engine.load_model()["threshold"],
        "predictions": results,
        "disclaimer": "Research demonstration only. Not for clinical use.",
    })


def api_features(request):
    return JsonResponse({"features": engine.load_model()["features"]})
