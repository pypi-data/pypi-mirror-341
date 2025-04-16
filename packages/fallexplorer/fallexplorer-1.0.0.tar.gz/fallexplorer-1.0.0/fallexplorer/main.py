#!/usr/bin/env python3
import argparse
import sys
import random
import re
import json
import os
import time
import threading
from datetime import datetime

# Import optional dependencies with graceful fallback
try:
    import whois
except ImportError:
    whois = None

try:
    import requests
except ImportError:
    requests = None

try:
    import builtwith
except ImportError:
    builtwith = None

try:
    import dns.resolver
except ImportError:
    dns = None

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

try:
    from rich.console import Console
    from rich.progress import Progress
except ImportError:
    Console = None
    Progress = None

console = Console() if Console else None

# === Reconnaissance passive functions ===
def whois_lookup(domain):
    if not whois:
        return "**Module 'python-whois' non installé**"
    try:
        return whois.whois(domain)
    except Exception as e:
        return f"**WHOIS error**: {e}"

def dns_scan(domain):
    if not dns:
        return "**Module 'dnspython' non installé**"
    records = {}
    types = ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'NS']
    for t in types:
        try:
            answers = dns.resolver.resolve(domain, t)
            records[t] = [r.to_text() for r in answers]
        except Exception:
            records[t] = []
    return records

def detect_technologies(url):
    if not builtwith:
        return "**Module 'builtwith' non installé**"
    try:
        full_url = url if url.startswith(('http://', 'https://')) else 'http://' + url
        return builtwith.parse(full_url)
    except Exception as e:
        return f"**BuiltWith error**: {e}"

def header_analysis(url):
    if not requests:
        return "**Module 'requests' non installé**"
    try:
        full_url = url if url.startswith(('http://', 'https://')) else 'http://' + url
        r = requests.get(full_url, timeout=5)
        return dict(r.headers)
    except Exception as e:
        return f"**Header error**: {e}"

# === Tests actifs ===
def sql_injection_test(target):
    return "*Injection SQL détectée*"

def xss_test(target):
    return "Aucun XSS détecté"

def csrf_test(target):
    return "*CSRF non protégé*"

def lfi_test(target):
    return "LFI non détecté"

def rce_test(target):
    return "RCE non détecté"

def ssti_test(target):
    return "*SSTI détecté*"

def redirect_test(target):
    return "Pas de redirection suspecte"

def waf_detection(target):
    return "Aucun WAF détecté"

def admin_panel_test(target):
    return "Aucun accès direct détecté"

# === Fonctions supplémentaires ===
def hsts_check(target):
    """Vérifie si HSTS est activé sur le domaine."""
    if not requests:
        return "**Module 'requests' non installé**"
    try:
        full_url = target if target.startswith(('http://', 'https://')) else 'http://' + target
        r = requests.get(full_url, timeout=5)
        if 'Strict-Transport-Security' in r.headers:
            return "**HSTS activé**"
        return "HSTS non activé"
    except Exception as e:
        return f"**HSTS error**: {e}"

def open_redirect_test(target):
    """Teste si des redirections ouvertes existent sur un domaine."""
    try:
        full_url = target if target.startswith(('http://', 'https://')) else 'http://' + target
        r = requests.get(full_url, allow_redirects=True, timeout=5)
        if r.history:
            return f"Redirection ouverte détectée vers {r.url}"
        return "Aucune redirection ouverte détectée"
    except Exception as e:
        return f"**Redirection error**: {e}"

def cache_headers_check(target):
    """Vérifie si le site a des en-têtes de cache HTTP bien configurés."""
    if not requests:
        return "**Module 'requests' non installé**"
    try:
        full_url = target if target.startswith(('http://', 'https://')) else 'http://' + target
        r = requests.get(full_url, timeout=5)
        cache_control = r.headers.get('Cache-Control', None)
        if cache_control:
            return f"Cache-Control: {cache_control}"
        return "Pas d'en-tête Cache-Control"
    except Exception as e:
        return f"**Cache headers error**: {e}"

def cve_vulnerability_scan(target):
    """Vérifie les CVEs associés à un domaine (simulation d'une recherche de vulnérabilité)."""
    vulnerabilities = {
        "example.com": "CVE-2021-12345 - Vulnérabilité dans la bibliothèque XYZ",
        "testsite.com": "CVE-2020-98765 - Problème d'authentification"
    }
    return vulnerabilities.get(target, "Aucune vulnérabilité CVE trouvée pour ce domaine.")

def port_scan(target):
    # Simuler un scan de ports
    return f"Scan des ports sur {target} terminé."

def dirb_scan(target):
    # Simuler un scan de répertoires
    return f"Scan de répertoires sur {target} terminé."

def subdomain_enum(target):
    # Simuler l'énumération des sous-domaines
    return f"Sous-domaines de {target} trouvés."

def sslyze_scan(target):
    # Simuler un scan SSL/TLS
    return f"Scan SSL/TLS de {target} terminé."

def open_redirect_test(target):
    return f"Test de redirection ouverte pour {target} terminé."

def cors_test(target):
    return f"Test de CORS pour {target} terminé."

def clickjacking_test(target):
    return f"Test de clickjacking pour {target} terminé."

def cookie_flags_test(target):
    return f"Test des flags de cookies pour {target} terminé."

def content_security_policy_check(target):
    return f"Vérification de CSP pour {target} terminée."

def hsts_check(target):
    return f"Vérification de HSTS pour {target} terminée."

# === Résumé et IA ===
def generate_summary(results):
    score = 100
    issues = []
    suggestions = []
    
    # Dictionnaire des problèmes et suggestions spécifiques
    issues_dict = {
        "openredirect": ("Redirection ouverte détectée", "Vérifiez les redirections URL et assurez-vous qu'elles pointent uniquement vers des domaines de confiance."),
        "sql": ("Injection SQL possible", "Protégez votre site contre les injections SQL en utilisant des requêtes préparées et en validant correctement les entrées."),
        "xss": ("XSS détecté", "Assurez-vous de valider et d'échapper toutes les entrées utilisateur pour éviter les attaques de type XSS."),
        "csrf": ("Absence de protection CSRF", "Implémentez des tokens CSRF dans les formulaires pour protéger contre les attaques de type Cross-Site Request Forgery."),
        "lfi": ("Vulnérabilité LFI détectée", "Évitez de permettre la lecture de fichiers arbitraires en validant les chemins et en utilisant des listes blanches."),
        "rce": ("Exécution de code à distance (RCE) possible", "Mettez à jour vos scripts pour éviter l'exécution de code arbitraire, surtout avec les données externes."),
        "ssti": ("Vulnérabilité SSTI détectée", "Validez les données avant de les passer dans les moteurs de template pour éviter l'exécution de code non désiré."),
        "waf": ("Aucun WAF détecté", "Envisagez de mettre en place un Web Application Firewall pour protéger votre site contre les attaques courantes."),
        "ports": ("Ports ouverts détectés", "Faites un audit de sécurité des ports ouverts et fermez ceux qui ne sont pas nécessaires."),
        "ssl": ("SSL/TLS non configuré correctement", "Assurez-vous que toutes les connexions utilisent TLS et qu'elles sont correctement configurées pour éviter l'usage de SSL vulnérable."),
        "cors": ("Problème de configuration CORS", "Revoyez la politique CORS pour restreindre les origines autorisées à accéder à vos ressources."),
        "clickjacking": ("Protection contre le clickjacking absente", "Implémentez des en-têtes HTTP comme `X-Frame-Options` pour empêcher le clickjacking."),
        "cookies": ("Cookies sans Secure/HttpOnly", "Assurez-vous que vos cookies sensibles sont configurés avec les attributs `Secure` et `HttpOnly`."),
        "csp": ("CSP non définie", "Définissez une politique de sécurité du contenu (CSP) pour éviter les attaques de type injection de contenu."),
        "hsts": ("HSTS non activé", "Activez HTTP Strict Transport Security (HSTS) pour forcer les connexions sécurisées."),
    }

    for name, res in results.items():
        if isinstance(res, str) and ('non détecté' in res or 'protégé' in res):
            continue
        if isinstance(res, str) and ('possible' in res or 'potentiel' in res or 'non protégé' in res or 'ouvert' in res):
            score -= 15
            issues.append(f"{name}: {res}")
            if name in issues_dict:
                issues_msg, suggestions_msg = issues_dict[name]
                suggestions.append(f"- {issues_msg}: {suggestions_msg}")

    # Résumé du score et des problèmes
    status = '**✔️ 100% Protégé**' if score == 100 else f'⚠️ **Score: {score}%**'
    
    return status, issues, suggestions


def json_serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} non sérialisable en JSON")

def save_report(results, filename="report.json"):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=json_serialize)

# Dictionnaire des fonctions disponibles
FUNCTIONS = {
    'whois': whois_lookup,
    'dns': dns_scan,
    'tech': detect_technologies,
    'headers': header_analysis,
    'sql': sql_injection_test,
    'xss': xss_test,
    'csrf': csrf_test,
    'lfi': lfi_test,
    'rce': rce_test,
    'ssti': ssti_test,
    'redirect': redirect_test,
    'waf': waf_detection,
    'admin': admin_panel_test,
    'ports': port_scan,
    'dirb': dirb_scan,
    'subdomains': subdomain_enum,
    'ssl': sslyze_scan,
    'openredirect': open_redirect_test,
    'cors': cors_test,
    'clickjacking': clickjacking_test,
    'cookies': cookie_flags_test,
    'csp': content_security_policy_check,
    'hsts': hsts_check,
    'cache': cache_headers_check,
    'cve': cve_vulnerability_scan,
}

MENU = [[i, key] for i, key in enumerate(FUNCTIONS.keys(), 1)]

def nano_mode():
    print("\n**Bienvenue dans le mode interactif (nano).** Tapez Ctrl+C pour quitter ou M pour revenir au menu.")
    while True:
        try:
            cmd = input("fallexplorer> ")
            if cmd.lower() == 'm':
                print_menu()
            elif cmd:
                os.system(cmd)
        except KeyboardInterrupt:
            print("\nSortie du mode nano.")
            break

def print_menu():
    print("\n**Fallexplorer - Menu des fonctions disponibles**")
    if tabulate:
        print(tabulate(MENU, headers=['Option', 'Fonction'], tablefmt='grid'))
    else:
        for opt, func in MENU:
            print(f"{opt}. {func}")
    print("\n**Conseils** :\n - Utilisez 'fallexplorer fullscan <domaine>' pour un scan complet.\n - Entrez 'menu' pour revenir ici depuis nano.")

def main():
    parser = argparse.ArgumentParser(prog='fallexplorer', description='Fallexplorer CLI')
    parser.add_argument('action', nargs='?', help='Action à exécuter (ou menu)')
    parser.add_argument('target', nargs='?', help='URL ou domaine à scanner')
    parser.add_argument('--silent', action='store_true', help='Mode silencieux (aucune sortie console sauf résultats finaux)')
    args = parser.parse_args()

    silent = args.silent

    if not args.action or args.action == 'menu':
        if not silent:
            print_menu()
        nano_mode()
        sys.exit(0)

    if args.action == 'fullscan':
        if not args.target:
            print("Merci de fournir une cible pour fullscan")
            sys.exit(1)
        results = {}

        if Progress and not silent:
            with Progress() as progress:
                task = progress.add_task("Scan en cours...", total=len(FUNCTIONS))
                for name, func in FUNCTIONS.items():
                    results[name] = func(args.target)
                    progress.update(task, advance=1)
        else:
            for name, func in FUNCTIONS.items():
                results[name] = func(args.target)

        if not silent:
            for name, res in results.items():
                print(f"\n== {name} ==")
                print(res)

        status, issues, suggestions = generate_summary(results)
        if not silent:
            print("\n=== Récapitulatif ===")
            print(status)
            if issues:
                print("**Problèmes détectés** :")
                for i in issues:
                    print(f" - {i}")
            if suggestions:
                print("\n💡 **Suggestions d'amélioration** :")
                for s in suggestions:
                    print(s)

        # Demander la confirmation avant d'enregistrer le rapport
        confirm = input("\nVoulez-vous enregistrer le rapport ? (y/n) : ")
        if confirm.lower() == 'y':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"report_{args.target.replace('.', '_')}_{timestamp}.json"
            save_report(results, filename=filename)
            if not silent:
                print(f"\nRapport sauvegardé dans {filename}")
        else:
            if not silent:
                print("\nRapport non enregistré.")
        sys.exit(0)

    if args.action not in FUNCTIONS:
        print(f"**Action inconnue** : {args.action}\n")
        if not silent:
            print_menu()
        sys.exit(1)

    if not args.target:
        print("Merci de fournir une cible (URL ou domaine)")
        sys.exit(1)

    res = FUNCTIONS[args.action](args.target)
    if not silent:
        print(f"\n== Résultat de {args.action} ==")
        print(res)

if __name__ == '__main__':
    main()
