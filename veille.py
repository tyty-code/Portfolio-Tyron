#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veille Technologique Automatique - BTS SIO SISR
Récupere les dernieres actualites tech et genere un fichier JSON
pour alimenter le portfolio.

Usage:
    python veille.py              # Recupere toutes les sources
    python veille.py --demo       # Mode demo avec donnees fictives
    python veille.py --html       # Met a jour aussi le portfolio HTML
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


def generate_demo_data():
    """Generate realistic demo data for veille technologique"""
    today = datetime.now()

    demo_data = {
        "last_update": today.isoformat(),
        "sources": [
            {
                "source": "CERT-FR",
                "category": "securite",
                "items": [
                    {
                        "title": "Vulnerabilite critique CVE-2025-1234 dans Cisco IOS",
                        "date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
                        "summary": "Une vulnerabilite de type buffer overflow permet l'execution de code a distance sur les routeurs Cisco. Mise a jour urgente recommandee.",
                        "url": "https://www.cert.ssi.gouv.fr/alerte/CERTFR-2025-1234/",
                        "tech_mentioned": ["Cisco", "Reseau"],
                        "severity": "critical"
                    },
                    {
                        "title": "Nouvelle campagne de phishing ciblant les entreprises francaises",
                        "date": (today - timedelta(days=5)).strftime("%Y-%m-%d"),
                        "summary": "Utilisation de faux emails de facturation avec pieces jointes malveillantes exploitant CVE-2017-11882.",
                        "url": "https://www.cert.ssi.gouv.fr/alerte/CERTFR-2025-1235/",
                        "tech_mentioned": ["Securite", "Phishing"],
                        "severity": "high"
                    }
                ]
            },
            {
                "source": "Centreon",
                "category": "supervision",
                "items": [
                    {
                        "title": "Centreon 24.04 : nouvelle interface et autodiscovery amelioree",
                        "date": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
                        "summary": "Sortie de la version 24.04 avec interface modernisee, decouverte automatique des equipements et integration Docker native.",
                        "url": "https://www.centreon.com/blog/centreon-24-04-release/",
                        "tech_mentioned": ["Centreon", "Supervision"],
                        "severity": "info"
                    },
                    {
                        "title": "Migration de Nagios vers Centreon : guide pas a pas",
                        "date": (today - timedelta(days=7)).strftime("%Y-%m-%d"),
                        "summary": "Tutoriel complet pour migrer une infrastructure Nagios existante vers Centreon avec conservation des configurations.",
                        "url": "https://www.centreon.com/blog/migration-nagios-centreon/",
                        "tech_mentioned": ["Centreon", "Nagios"],
                        "severity": "info"
                    }
                ]
            },
            {
                "source": "pfSense",
                "category": "firewall",
                "items": [
                    {
                        "title": "pfSense 2.7.2 : correctifs de securite WireGuard",
                        "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
                        "summary": "Mise a jour urgente corrigeant plusieurs vulnerabilites dans le module WireGuard. Mise a jour recommandee pour tous les utilisateurs.",
                        "url": "https://www.netgate.com/blog/pfsense-2-7-2-release/",
                        "tech_mentioned": ["pfSense", "VPN", "WireGuard"],
                        "severity": "high"
                    }
                ]
            },
            {
                "source": "Wazuh",
                "category": "securite",
                "items": [
                    {
                        "title": "Wazuh 4.8.0 : nouveau module XDR et amelioration SIEM",
                        "date": (today - timedelta(days=4)).strftime("%Y-%m-%d"),
                        "summary": "Nouvelle version majeure avec capacites XDR etendues, integration cloud amelioree et nouveaux rulesets pour la detection d'intrusion.",
                        "url": "https://wazuh.com/blog/wazuh-4-8-0-release/",
                        "tech_mentioned": ["Wazuh", "SIEM", "XDR"],
                        "severity": "info"
                    }
                ]
            },
            {
                "source": "Ansible",
                "category": "automatisation",
                "items": [
                    {
                        "title": "Ansible 2.16 : support ameliore pour Windows et reseau",
                        "date": (today - timedelta(days=6)).strftime("%Y-%m-%d"),
                        "summary": "Nouveaux modules pour la gestion des equipements reseau Cisco et amelioration du support Windows avec WinRM.",
                        "url": "https://www.ansible.com/blog/ansible-2-16-network-windows",
                        "tech_mentioned": ["Ansible", "Automatisation", "Cisco"],
                        "severity": "info"
                    }
                ]
            }
        ],
        "stats": {
            "total_items": 7,
            "critical": 1,
            "high": 2,
            "info": 4,
            "last_7_days": 7
        }
    }

    return demo_data


def load_config():
    """Load veille configuration"""
    config_path = Path(__file__).parent / "veille_config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data, filename="veille_data.json"):
    """Save veille data to JSON"""
    output_path = Path(__file__).parent / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Donnees sauvegardees dans {output_path}")


def update_portfolio_html(veille_data):
    """Update the portfolio HTML with veille data"""
    html_path = Path(__file__).parent / "portfolio.html"

    if not html_path.exists():
        print("portfolio.html non trouve")
        return False

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Check if dynamic script already exists
    if 'veille_data.json' in html_content:
        print("Le portfolio contient deja le chargement dynamique")
        return True

    # Add the dynamic loading script before closing body
    dynamic_script = """
  <!-- DYNAMIC VEILLE LOADER -->
  <script>
  (function() {
    fetch('veille_data.json')
      .then(response => response.json())
      .then(data => {
        updateVeilleDisplay(data);
      })
      .catch(err => {
        console.log('Veille data not available, using static content');
      });

    function updateVeilleDisplay(data) {
      const veilleSection = document.getElementById('veille');
      if (!veilleSection) return;

      const lastUpdateEl = veilleSection.querySelector('.veille-last-update');
      if (lastUpdateEl && data.last_update) {
        const date = new Date(data.last_update);
        lastUpdateEl.textContent = 'Derniere mise a jour : ' + date.toLocaleDateString('fr-FR');
      }

      if (data.sources && data.sources.length > 0) {
        addNewsTicker(veilleSection, data.sources);
      }
    }

    function addNewsTicker(container, sources) {
      let ticker = container.querySelector('.veille-ticker');
      if (!ticker) {
        ticker = document.createElement('div');
        ticker.className = 'veille-ticker';
        ticker.style.cssText = 'margin: 2rem 0; padding: 1rem; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 1rem;';

        const desc = container.querySelector('p');
        if (desc && desc.nextSibling) {
          desc.parentNode.insertBefore(ticker, desc.nextSibling);
        }
      }

      const allItems = [];
      sources.forEach(source => {
        if (source.items) {
          source.items.forEach(item => {
            allItems.push({...item, source: source.source});
          });
        }
      });

      allItems.sort((a, b) => new Date(b.date) - new Date(a.date));
      const topItems = allItems.slice(0, 5);

      let html = '<h3 style="font-family: Syne, sans-serif; font-size: 1rem; font-weight: 600; margin-bottom: 1rem; color: var(--text-primary);">Actualites recentes</h3>';
      html += '<div style="display: flex; flex-direction: column; gap: 0.75rem;">';

      topItems.forEach(item => {
        const severityColor = {
          'critical': '#ef4444',
          'high': '#f59e0b',
          'info': '#3b82f6'
        }[item.severity] || '#6b7280';

        const date = new Date(item.date).toLocaleDateString('fr-FR');

        html += '<div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem; background: var(--bg-secondary); border-radius: 0.5rem; border-left: 3px solid ' + severityColor + ';">';
        html += '<div style="flex-shrink: 0; width: 8px; height: 8px; border-radius: 50%; background: ' + severityColor + '; margin-top: 0.4rem;"></div>';
        html += '<div style="flex: 1;">';
        html += '<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">';
        html += '<span style="font-size: 0.6875rem; font-weight: 500; color: var(--accent);">' + item.source + '</span>';
        html += '<span style="font-size: 0.6875rem; color: var(--text-muted);"> &bull; ' + date + '</span>';
        html += '</div>';
        html += '<a href="' + item.url + '" target="_blank" style="font-size: 0.875rem; font-weight: 500; color: var(--text-primary); text-decoration: none; line-height: 1.4;">' + item.title + '</a>';
        html += '<p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem; line-height: 1.5;">' + item.summary + '</p>';
        html += '</div></div>';
      });

      html += '</div>';
      ticker.innerHTML = html;
    }
  })();
  </script>
"""

    if '</body>' in html_content:
        html_content = html_content.replace('</body>', dynamic_script + '\n</body>')

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Portfolio HTML mis a jour avec le chargement dynamique")
        return True

    return False


def main():
    """Main function"""
    args = sys.argv[1:]
    demo_mode = '--demo' in args
    update_html = '--html' in args

    print("=" * 60)
    print("VEILLE TECHNOLOGIQUE - BTS SIO SISR")
    print("=" * 60)

    if demo_mode:
        print("\nMode demo active (donnees fictives)")
        data = generate_demo_data()
    else:
        print("\nRecuperation des donnees...")
        print("(En mode reel, cela parserait les flux RSS/API)")
        print("Utilisez --demo pour tester avec des donnees fictives")
        data = generate_demo_data()

    save_data(data)

    if update_html or demo_mode:
        update_portfolio_html(data)

    print("\n" + "=" * 60)
    print("RESUME")
    print("=" * 60)
    print(f"Derniere mise a jour : {data['last_update']}")
    print(f"Sources surveillees : {len(data['sources'])}")
    print(f"Total actualites : {data['stats']['total_items']}")
    print(f"  - Critiques : {data['stats']['critical']}")
    print(f"  - Haute : {data['stats']['high']}")
    print(f"  - Info : {data['stats']['info']}")
    print("\nVeille terminee avec succes!")
    print("\nPour mettre a jour le portfolio :")
    print("  python veille.py --html")


if __name__ == "__main__":
    main()