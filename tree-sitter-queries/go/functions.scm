(function_declaration
  name: (identifier) @function.name
  body: (_) @function.body
) @function

(method_declaration
  name: (field_identifier) @function.name
  body: (_) @function.body
) @function
