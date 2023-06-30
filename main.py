from save import save_as_csv
import head_hunter

hhVacancies = head_hunter.ExtractAllVacancies(vacancy="подработка")
save_as_csv(hhVacancies)