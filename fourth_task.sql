select name, (contracts.tax_percentage * positions.salary / 100) from employees
join contracts on contracts.id = employees.conract_id
join positions on positions.id = employees.position_id
where positions.salary < 50000
