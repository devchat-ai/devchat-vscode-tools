(class_declaration
  (constructor
    normal_formal_parameters: (normal_formal_parameter_list
      normal_formal_parameter: (normal_formal_parameter
        name: (identifier) @variable
      )
    )
  )
)

(function_declaration
  formal_parameter_list: (formal_parameter_list
    normal_formal_parameters: (normal_formal_parameter_list
      normal_formal_parameter: (normal_formal_parameter
        name: (identifier) @variable
      )
    )
  )
)

(field_formal_parameters
  field_formal_parameter: (field_formal_parameter
    name: (identifier) @variable
  )
)

(variable_declaration_list
  variable_declaration: (variable_declaration
    name: (identifier) @variable
  )
)
