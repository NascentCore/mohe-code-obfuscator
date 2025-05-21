import { DataSource } from "typeorm"
import ormconfig from "./ormconfig"
export const AppDataSource = new DataSource({
    ...ormconfig,
    type: "postgres" as const
}) 