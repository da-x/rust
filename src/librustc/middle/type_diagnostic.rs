// Type diagnostic.
//
// This controls how types are being presented to the user upon errors.

use crate::session::{TypeDiagnosticKind, Session};
use syntax::symbol::sym;

impl std::str::FromStr for TypeDiagnosticKind {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, ()> {
        let mode = match s {
            "uniform" => TypeDiagnosticKind::Uniform,
            "by-import" => TypeDiagnosticKind::ByUse,
            "minimal" => TypeDiagnosticKind::Minimal,
            _ => return Err(())
        };
        Ok(mode)
    }
}

pub fn update(sess: &Session, krate: &syntax::ast::Crate) {
    for attr in &krate.attrs {
        if !attr.check_name(sym::type_diagnostic) {
            continue;
        }

        if let Some(s) = attr.value_str() {
            match s.as_str().parse() {
                Ok(value) => sess.type_diagnostic.set(value),
                Err(_) => sess.fatal(&format!(
                    "Invalid value for attribute `type_diagnostic`, needs either of {:?}",
                    ["uniform", "by-import", "minimal"],
                )),
            }
            return;
        }
    }

    sess.type_diagnostic.set(TypeDiagnosticKind::Minimal);
}
