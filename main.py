from save import save_as_csv
import head_hunter

hhVacancies = head_hunter.ExtractAllVacancies(vacancy="Ступино")
save_as_csv(hhVacancies)