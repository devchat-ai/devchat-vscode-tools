(import_statement
    (import_clause
      (identifier)* @import.type
      (named_imports
        (import_specifier
          (identifier) @import.type
        )
      )*
      (namespace_import
       (identifier) @import.type
      )*
    )
)

(assignment_expression
  (member_expression
    object: (this)
    property: (property_identifier) @variable
  ))

(variable_declarator
  name: (identifier) @variable
)

(formal_parameters
    (identifier) @variable
)