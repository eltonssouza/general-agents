# -*- coding: utf-8 -*-
"""
rails_store_checklist.py - checklist of the "store" app built in the RGS guide (Rails 8.1.0+).
The guide builds the "store" (not a "blog"). STATIC, read-only inspection of a Rails app directory:
does not execute Ruby/Rails, does not access the network. File contents are DATA.

Usage:
  python -I scripts/rails_store_checklist.py --list
  python -I scripts/rails_store_checklist.py APP_DIR [--json] [--ate S25]
Result per item: OK, MISSING, MANUAL (the script cannot verify). Passing does not prove correctness or security;
it only indicates that the app follows the shape of the tutorial. Exit 0 if no MISSING, 1 otherwise.
Page convention: PDF = "Page N of 72".
"""
import argparse
import glob
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def rd(root, rel):
    p = os.path.join(root, rel)
    if os.path.isfile(p):
        return open(p, "r", encoding="utf-8", errors="replace").read()
    return None


def rd_glob(root, pattern):
    out = []
    for p in glob.glob(os.path.join(root, pattern), recursive=True):
        if os.path.isfile(p):
            out.append(open(p, "r", encoding="utf-8", errors="replace").read())
    return out


def has(t, rx):
    return t is not None and re.search(rx, t, re.S) is not None


def product_text(root):
    parts = [rd(root, "app/models/product.rb") or ""]
    parts += rd_glob(root, "app/models/product/*.rb")
    return "\n".join(parts)


def c_s02(r):
    t = rd(r, "app/models/product.rb")
    return has(t, r"class\s+Product\s*<\s*ApplicationRecord")


def c_s03(r):
    ms = rd_glob(r, "db/migrate/*create_products*.rb")
    return any(has(m, r"create_table\s+:products") and has(m, r"t\.string\s+:name") and has(m, r"t\.timestamps") for m in ms)


def c_s04(r):
    return has(product_text(r), r"validates\s+:name,\s*presence:\s*true")


def c_s05(r):
    return has(rd(r, "config/routes.rb"), r"resources\s+:products")


def c_s06(r):
    return has(rd(r, "config/routes.rb"), r"root\s+[\"']products#index[\"']")


def c_s07(r):
    t = rd(r, "app/controllers/products_controller.rb")
    return t is not None and all(has(t, rf"def\s+{a}\b") for a in ["index", "show", "new", "create", "edit", "update", "destroy"])


def c_s08(r):
    return has(rd(r, "app/controllers/products_controller.rb"), r"params\.expect\(\s*product:")


def c_s09(r):
    return has(rd(r, "app/controllers/products_controller.rb"), r"before_action\s+:set_product")


def c_s10(r):
    t = rd(r, "app/controllers/products_controller.rb")
    return has(t, r"render\s+:new,\s*status:\s*:unprocessable_entity") and has(t, r"render\s+:edit,\s*status:\s*:unprocessable_entity")


def c_s11(r):
    return all(os.path.isfile(os.path.join(r, "app/views/products", f)) for f in
               ["index.html.erb", "show.html.erb", "new.html.erb", "edit.html.erb", "_form.html.erb"])


def c_s12(r):
    return has(rd(r, "app/views/products/_form.html.erb"), r"form_with\s+model:\s*product")


def c_s13(r):
    return (os.path.isfile(os.path.join(r, "app/models/user.rb")) and os.path.isfile(os.path.join(r, "app/models/session.rb"))
            and has(rd(r, "app/controllers/products_controller.rb"), r"allow_unauthenticated_access\s+only:\s*%i\[\s*index\s+show\s*\]"))


def c_s14(r):
    t = rd(r, "app/views/layouts/application.html.erb")
    return has(t, r"<nav>") and has(t, r"button_to\s+[\"']Log out[\"'].*authenticated\?")


def c_s15(r):
    return has(rd(r, "app/views/products/show.html.erb"), r"cache\s+@product\s+do")


def c_s16(r):
    return has(product_text(r), r"has_rich_text\s+:description") and has(rd(r, "app/controllers/products_controller.rb"), r":description")


def c_s17(r):
    return has(product_text(r), r"has_one_attached\s+:featured_image") and has(rd(r, "app/controllers/products_controller.rb"), r":featured_image")


def c_s18(r):
    return (os.path.isfile(os.path.join(r, "config/locales/en.yml")) and os.path.isfile(os.path.join(r, "config/locales/es.yml"))
            and has(rd(r, "app/controllers/application_controller.rb"), r"around_action\s+:switch_locale"))


def c_s19(r):
    ms = rd_glob(r, "db/migrate/*inventory_count*.rb")
    return (any(has(m, r"add_column\s+:products,\s*:inventory_count,\s*:integer,\s*default:\s*0") for m in ms)
            and has(product_text(r), r"validates\s+:inventory_count,\s*numericality:"))


def c_s20(r):
    s = rd(r, "app/models/subscriber.rb")
    return has(s, r"belongs_to\s+:product") and has(product_text(r), r"has_many\s+:subscribers,\s*dependent:\s*:destroy")


def c_s21(r):
    return (os.path.isfile(os.path.join(r, "app/controllers/subscribers_controller.rb"))
            and has(rd(r, "config/routes.rb"), r"resources\s+:subscribers,\s*only:\s*\[\s*:create\s*\]"))


def c_s22(r):
    m = rd(r, "app/mailers/product_mailer.rb")
    h = rd(r, "app/views/product_mailer/in_stock.html.erb")
    t = rd(r, "app/views/product_mailer/in_stock.text.erb")
    return has(m, r"def\s+in_stock") and has(h, r"product_url") and has(t, r"product_url")


def c_s23(r):
    return has(product_text(r), r"after_update_commit\s+:notify_subscribers,\s*if:\s*:back_in_stock\?")


def c_s24(r):
    return has(rd(r, "app/models/product/notifications.rb"), r"extend\s+ActiveSupport::Concern")


def c_s25(r):
    return (has(rd(r, "config/routes.rb"), r"resource\s+:unsubscribe")
            and has(rd(r, "app/models/subscriber.rb"), r"generates_token_for\s+:unsubscribe")
            and os.path.isfile(os.path.join(r, "app/controllers/unsubscribes_controller.rb")))


def c_s26(r):
    return os.path.isfile(os.path.join(r, "app/assets/stylesheets/application.css")) and os.path.isfile(os.path.join(r, "config/importmap.rb"))


def c_s27(r):
    return (os.path.isfile(os.path.join(r, "test/fixtures/products.yml")) and os.path.isfile(os.path.join(r, "test/fixtures/subscribers.yml"))
            and has(rd(r, "test/models/product_test.rb"), r"assert_emails"))


def c_s29(r):
    return has(rd(r, "config/deploy.yml"), r"service:\s*store")


ITEMS = [
    ("S01", "Ruby 3.2+ and Rails 8.1.0+", "2", None),
    ("S02", "Model Product < ApplicationRecord", "8, 11", c_s02),
    ("S03", "Migration create_products (create_table, t.string :name, t.timestamps)", "8-9", c_s03),
    ("S04", "validates :name, presence: true", "16", c_s04),
    ("S05", "resources :products", "21", c_s05),
    ("S06", "root \"products#index\"", "23", c_s06),
    ("S07", "Actions index/show/new/create/edit/update/destroy", "22-37", c_s07),
    ("S08", "Strong params with params.expect(product: ...)", "30", c_s08),
    ("S09", "before_action :set_product", "34-37", c_s09),
    ("S10", "render :new/:edit with status: :unprocessable_entity", "30-32", c_s10),
    ("S11", "Views index/show/new/edit/_form", "23-34", c_s11),
    ("S12", "form_with model: product in the partial", "33", c_s12),
    ("S13", "Authentication (User, Session) and allow_unauthenticated_access only: %i[ index show ]", "38-40", c_s13),
    ("S14", "Layout with <nav> and Log out if authenticated?", "39-40", c_s14),
    ("S15", "cache @product do in the show view", "41", c_s15),
    ("S16", "has_rich_text :description and :description permitted", "43", c_s16),
    ("S17", "has_one_attached :featured_image and :featured_image permitted", "44-45", c_s17),
    ("S18", "I18n: en.yml, es.yml and around_action :switch_locale", "45-47", c_s18),
    ("S19", "Inventory: add_column default: 0 and numericality", "47-48", c_s19),
    ("S20", "Subscriber belongs_to :product; Product has_many :subscribers, dependent: :destroy", "49-50", c_s20),
    ("S21", "SubscribersController and nested route only: [ :create ]", "50-51", c_s21),
    ("S22", "ProductMailer#in_stock with HTML/text views using product_url", "52-53", c_s22),
    ("S23", "after_update_commit :notify_subscribers, if: :back_in_stock?", "56", c_s23),
    ("S24", "Concern Product::Notifications", "57-58", c_s24),
    ("S25", "Unsubscribe: resource, generates_token_for, controller", "58-59", c_s25),
    ("S26", "CSS (application.css) and importmap.rb", "60-63", c_s26),
    ("S27", "Fixtures and test with assert_emails", "64-66", c_s27),
    ("S28", "bin/rubocop and bin/brakeman with no offenses", "66-67", None),
    ("S29", "config/deploy.yml with service: store", "68-69", c_s29),
    ("S30", "bin/kamal setup, user in production, Solid Queue", "69-70", None),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app_dir", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ate", default="S30", help="last item to check (e.g. S12 to stop at the CRUD)")
    a = ap.parse_args()
    if a.list:
        for i, d, p, f in ITEMS:
            print(f"{i} RGS p.{p:7} {d}" + ("" if f else "  [manual]"))
        return
    if not a.app_dir:
        ap.print_help()
        sys.exit(2)
    if not os.path.isdir(a.app_dir):
        print(f"ERROR: directory not found: {a.app_dir}")
        sys.exit(2)
    limit = int(re.sub(r"\D", "", a.ate) or 30)
    res = []
    falta = 0
    for i, d, p, f in ITEMS:
        if int(i[1:]) > limit:
            continue
        if f is None:
            st = "MANUAL"
        else:
            try:
                st = "OK" if f(a.app_dir) else "MISSING"
            except Exception as e:  # defensive read
                st = "MISSING"
        if st == "MISSING":
            falta += 1
        res.append({"id": i, "item": d, "pagina": f"RGS p.{p}", "status": st})
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for r in res:
            print(f"{r['id']} [{r['status']:6}] {r['pagina']:12} {r['item']}")
        ok = sum(1 for r in res if r["status"] == "OK")
        print(f"Summary: {ok} OK, {falta} MISSING, {sum(1 for r in res if r['status']=='MANUAL')} MANUAL. "
              "The checklist indicates adherence to the shape of the 'store' tutorial, not correctness or security.")
    sys.exit(1 if falta else 0)


if __name__ == "__main__":
    main()
