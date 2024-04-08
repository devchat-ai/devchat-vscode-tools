(function_definition
  (function_declarator
    declarator: (identifier) @function.name
  )
  body: (_) @function.body
) @function

(function_definition
  (function_declarator
    declarator: (field_identifier) @function.name
  )
  body: (_) @function.body
) @function