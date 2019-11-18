/*

  Copyright 2017 Loopring Project Ltd (Loopring Foundation).

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/
pragma solidity ^0.5.11;

import "../iface/Wallet.sol";
import "../iface/Module.sol";

import "../lib/ReentrancyGuard.sol";


/// @title BaseModule
/// @dev This contract implements some common functions that are likely
///      be useful for all modules.
///
/// @author Daniel Wang - <daniel@loopring.org>
///
/// The design of this contract is inspired by Argent's contract codebase:
/// https://github.com/argentlabs/argent-contracts
contract BaseModule is Module, ReentrancyGuard
{
    /// @dev Adds a module to a wallet. Callable only by the wallet owner.
    function addModule(
        address wallet,
        address module
        )
        external
        nonReentrant
        onlyStricklyWalletOwner(wallet)
    {
        Wallet(wallet).addModule(module);
    }

    /// @dev Adds a module to a wallet. Callable only by the wallet owner.
    function removeModule(
        address wallet,
        address module
        )
        external
        nonReentrant
        onlyStricklyWalletOwner(wallet)
    {
        Wallet(wallet).removeModule(module);
    }

    /// @dev Bind a static method to the  wallet. Callable only by the wallet owner.
    function bindStaticMethod(address wallet, bytes4 method, address module)
        external
        nonReentrant
        onlyStricklyWalletOwner(wallet)
    {
        Wallet(wallet).bindStaticMethod(method, module);
    }

    /// @dev Internal method to transact on the given wallet.
    function transact(
        address wallet,
        address to,
        uint    value,
        bytes   memory data
        )
        internal
        returns (bytes memory result)
    {
        // Optimize for gas usage when data is large?
        return Wallet(wallet).transact(to, value, data);
    }
}