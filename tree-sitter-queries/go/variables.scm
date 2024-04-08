(var_declaration
  (var_spec
    name: (identifier) @variable
))

(short_var_declaration
  left: (expression_list
    (identifier) @variable
))

(parameter_list
  (parameter_declaration
    (identifier) @variable
))

(field_declaration_list
  (field_declaration
    name: (field_identifier) @variable
))
