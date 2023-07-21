export interface Account {
    readonly accountId: string;
    readonly region: string;
    readonly stage: string;
    readonly airportCode: string;
}

export const Accounts: Account[] = [
    {
        accountId: '343102482966',
        stage: 'SAMSUNG',
        region: 'ap-northeast-2',
        airportCode: 'ICN',
    },
];

export function getAccountUniqueName(account: Account): string {
    return getAccountUniqueNameWithDelimiter(account, '-')
}

export function getAccountUniqueNameWithDelimiter(account: Account, delimiter: string): string {
    return `${account.stage}${delimiter}${account.airportCode}`
}

export function getDevAccount(userId: string): Account | undefined {
    return Accounts.find((account: Account) => { return account.stage === userId })
}