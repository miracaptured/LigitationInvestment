export class Case {
    case_id!: number;
    name: string = "";
    status: string = "";
    initiator_role: string = "";
    claim: number = 0;
    description: string = "";
    investment: number = 0;

    constructor(
        case_id: number,
        name: string,
        status: string,
        claim: number,
        description: string,
        investment: number,
        initiator_role: string)
        {
            this.case_id = case_id;
            this.name = name;
            this.status = status;
            this.claim = claim;
            this.description = description;
            this.investment = investment;
            this.initiator_role = initiator_role;
    }
}