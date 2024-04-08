(import_from_statement
  name: (dotted_name
    (identifier) @import.type
))

(import_from_statement
  name: (aliased_import
  name: (dotted_name
    (identifier) @import.type
)))


(expression_statement
  (assignment
    left: (identifier) @variable
))

(expression_statement
  (assignment
    left: (pattern_list
    	(identifier) @variable
    )
))

(parameters
  (typed_parameter
    (identifier) @variable
  )
)

(parameters
  (typed_default_parameter
    name: (identifier) @variable
  )
)

(parameters
  (default_parameter
    (identifier) @variable
  )
)

(parameters
  (identifier) @variable
)


(expression_statement
  (assignment
    left: (attribute
      object: (identifier) @variable.object
      attribute: (identifier) @variable
    )
    (#eq? @variable.object "self")
))