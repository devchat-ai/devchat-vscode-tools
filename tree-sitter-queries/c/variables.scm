(declaration
  declarator: (init_declarator
    declarator: (identifier) @variable
))

(declaration
  declarator: (identifier) @variable
)

(declaration
  declarator: (init_declarator
    declarator: (array_declarator
      declarator: (identifier) @variable
)))

(declaration
  declarator: (init_declarator
    declarator: (pointer_declarator
      declarator: (identifier) @variable
)))

(parameter_list
  (parameter_declaration
    declarator: (identifier) @variable
))

(parameter_list
  (parameter_declaration
    declarator: (array_declarator
      declarator: (identifier) @variable
)))

(parameter_list
  (parameter_declaration
    declarator: (pointer_declarator
      declarator: (identifier) @variable
)))
