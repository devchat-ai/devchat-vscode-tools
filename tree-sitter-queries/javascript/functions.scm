(method_definition
  name: (property_identifier) @function.name
  body: (_) @function.body
) @function

(function_declaration
  name: (identifier) @function.name
  body: (_) @function.body
) @function

(function_expression
  name: (identifier) @function.name
  body: (_) @function.body
) @function

(generator_function_declaration
  name: (identifier) @function.name
  body: (_) @function.body
) @function