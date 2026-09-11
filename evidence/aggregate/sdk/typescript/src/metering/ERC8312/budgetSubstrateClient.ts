import {
  createPublicClient,
  http,
  type Account,
  type Hex,
  type PublicClient,
} from 'viem'
import { foundry } from 'viem/chains'
import { budgetSubstrateAbi } from './abi.js'
import type { ClientConfig } from './types.js'

export interface Bound {
  cap: bigint
  asset: `0x${string}`
}

export class BudgetSubstrateClient {
  private readonly publicClient: PublicClient
  private readonly address: ClientConfig['address']
  private readonly abi = budgetSubstrateAbi

  constructor(config: ClientConfig, _account?: Account) {
    const transport = http(config.rpcUrl)
    this.publicClient = createPublicClient({ chain: foundry, transport })
    this.address = config.address
  }

  async bound(id: Hex): Promise<Bound> {
    const result = await this.read('bound', [id]) as [bigint, `0x${string}`]
    return { cap: result[0], asset: result[1] }
  }

  async spent(id: Hex): Promise<bigint> {
    return this.read('spent', [id]) as Promise<bigint>
  }

  async remaining(id: Hex): Promise<bigint> {
    return this.read('remaining', [id]) as Promise<bigint>
  }

  private async read<T>(functionName: string, args: unknown[]): Promise<T> {
    return this.publicClient.readContract({
      address: this.address,
      abi: this.abi,
      functionName,
      args,
    } as never) as Promise<T>
  }
}
